import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.core import mail
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError
from .validators import validador_palabras_ofensivas

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption, Preference, Apportionment
from datetime import datetime

class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')

    def test_email_notification(self):
        voting = self.create_voting()
        self.login()

        # Testear que la acción start envía un correo
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')
        self.assertEqual(len(mail.outbox), 1)  # Asumimos que se envió un email
        self.assertIn('Una votación ha empezado', mail.outbox[0].subject)  # Chequeamos asunto del email

        # Testear que la acción stop no envía un correo
        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')
        self.assertEqual(len(mail.outbox), 1)  # Asumimos que no se envió ningún email

        # Testear que la acción tally envía un correo
        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')
        self.assertEqual(len(mail.outbox), 2)  # Asumimos que hay 2 emails
        self.assertIn('Resultados de votación', mail.outbox[1].subject)  # Chequeamos asunto del segundo email

    def test_voting_name_and_desc_validator(self):
        question = Question(desc="Esta es una pregunta sin palabras ofensivas")
        question.clean()

        voting = Voting(
            name="Votación sin palabras ofensivas",
            desc="Descripción de votación sin palabras ofensivas",
            question=question
        )
        voting.clean()

        voting_with_offensive_name = Voting(
            name="Votación con una palabra ofensiva: idiota",
            desc="Descripción de votación sin palabras ofensivas",
            question=question
        )
        with self.assertRaises(ValidationError):
            voting_with_offensive_name.clean()

        voting_with_offensive_desc = Voting(
            name="Votación sin palabras ofensivas",
            desc="Descripción de votación con una palabra ofensiva: idiota",
            question=question
        )
        with self.assertRaises(ValidationError):
            voting_with_offensive_desc.clean()

class LogInSuccessTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def successLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")
        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/")

class LogInErrorTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def usernameWrongLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("usuarioNoExistente")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("usuarioNoExistente")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/p').text == 'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.')

    def passwordWrongLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("wrongPassword")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/p').text == 'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.')

class QuestionsTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def createQuestionSuccess(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.cleaner.get(self.live_server_url+"/admin/voting/question/add/")

        self.cleaner.find_element(By.ID, "id_desc").click()
        self.cleaner.find_element(By.ID, "id_desc").send_keys('Test')
        self.cleaner.find_element(By.ID, "id_options-0-number").click()
        self.cleaner.find_element(By.ID, "id_options-0-number").send_keys('1')
        self.cleaner.find_element(By.ID, "id_options-0-option").click()
        self.cleaner.find_element(By.ID, "id_options-0-option").send_keys('test1')
        self.cleaner.find_element(By.ID, "id_options-1-number").click()
        self.cleaner.find_element(By.ID, "id_options-1-number").send_keys('2')
        self.cleaner.find_element(By.ID, "id_options-1-option").click()
        self.cleaner.find_element(By.ID, "id_options-1-option").send_keys('test2')
        self.cleaner.find_element(By.NAME, "_save").click()

        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/voting/question/")


    def createCensusEmptyError(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.cleaner.get(self.live_server_url+"/admin/voting/question/add/")

        self.cleaner.find_element(By.NAME, "_save").click()

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div/form/div/p').text == 'Please correct the errors below.')
        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/voting/question/add/")


    def test_question_desc_validator(self):
        pregunta = Question(desc="Esta es una pregunta sin palabras ofensivas")
        pregunta.clean()

        pregunta_ofensiva = Question(desc="Esta es una pregunta con una palabra ofensiva: cabrona")
        with self.assertRaises(ValidationError):
            pregunta_ofensiva.clean()


    def test_question_option_validator(self):
        question = Question(desc="Esta es una pregunta sin palabras ofensivas")
        question.clean()

        option = QuestionOption(question=question, option="Opción sin palabras ofensivas")
        option.clean()

        option_with_offensive_text = QuestionOption(question=question, option="Opción con una palabra ofensiva: idiota")
        with self.assertRaises(ValidationError):
            option_with_offensive_text.clean()

class ValidatorsTest(TestCase):

    def test_validador_palabras_ofensivas_validator_negativo(self):
        with self.assertRaises(ValidationError) as context:
            validador_palabras_ofensivas("Eres un gilipollas")
        self.assertEqual(
            context.exception.message,
            "Las palabras gilipollas no están permitidas."
        )

    def test_validator_palabras_ofensivas_validator_negativo_con_acentos(self):
        with self.assertRaises(ValidationError) as context:
            validador_palabras_ofensivas("Tú eres un imbécil")
        self.assertEqual(
            context.exception.message,
            "Las palabras imbécil, imbecil no están permitidas."
        )

    def test_validator_palabras_ofensivas_validator_negativo_varias_palabras(self):
        with self.assertRaises(ValidationError) as context:
            validador_palabras_ofensivas("Este texto contiene las palabras puto y idiota.")
        self.assertIn("puto", context.exception.message)
        self.assertIn("idiota", context.exception.message)

# Tests de count

class CountTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sort_preference_method(self):
        # Crear objetos de prueba
        question = Question.objects.create(desc='Test question')
        voting = Voting.objects.create(name='Test Voting', question=question)
        preference = Preference.objects.create(voting_id=voting.id)

        # Simular el postprocesamiento
        postproc_list = [
            {'option': 'Option 1', 'number': 1, 'postproc': 10},
            {'option': 'Option 2', 'number': 2, 'postproc': 16},
            {'option': 'Option 3', 'number': 3, 'postproc': 12},
            {'option': 'Option 4', 'number': 4, 'postproc': 5}
        ]
        voting.postproc = postproc_list
        voting.save()

        # Llamar al método sort y verificar el resultado
        preference.sort(voting)

        expected_result = "1- Option 2(2): 16,\n 2- Option 3(3): 12,\n 3- Option 1(1): 10,\n 4- Option 4(4): 5"
        self.assertEqual(preference.solution, expected_result)


    def test_dhondt_method(self):
        # Crear objetos de prueba
        question = Question.objects.create(desc='Test question')
        voting = Voting.objects.create(name='Test Voting', question=question)
        apportionment = Apportionment.objects.create(voting_id=voting.id, seats=7)

        # Simular el postprocesamiento
        postproc_list = [
            {'option': 'Option 1', 'number': 1, 'postproc': 340},
            {'option': 'Option 2', 'number': 2, 'postproc': 280},
            {'option': 'Option 3', 'number': 3, 'postproc': 160},
            {'option': 'Option 4', 'number': 4, 'postproc': 60}
        ]
        voting.postproc = postproc_list
        voting.save()

        # Verificar el resultado esperado y verificar el resultado
        apportionment.dhondt(voting)

        expected_result = "Option 1(1): 3, Option 2(2): 3, Option 3(3): 1, Option 4(4): 0"
        self.assertEqual(apportionment.solution, expected_result)


    def test_sainte_lague_method(self):
        # Crear objetos de prueba
        question = Question.objects.create(desc='Test question')
        voting = Voting.objects.create(name='Test Voting', question=question)
        apportionment = Apportionment.objects.create(voting_id=voting.id, seats=7)

        # Simular el postprocesamiento
        postproc_list = [
            {'option': 'Option 1', 'number': 1, 'postproc': 340},
            {'option': 'Option 2', 'number': 2, 'postproc': 280},
            {'option': 'Option 3', 'number': 3, 'postproc': 160},
            {'option': 'Option 4', 'number': 4, 'postproc': 60}
        ]
        voting.postproc = postproc_list
        voting.save()

        # Verificar el resultado esperado y verificar el resultado
        apportionment.sainte_lague(voting)

        expected_result = "Option 1(1): 3, Option 2(2): 2, Option 3(3): 1, Option 4(4): 1"
        self.assertEqual(apportionment.solution, expected_result)


class CountNegativeTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sort_preference_method_no_postproc(self):
        # Crear objetos de prueba
        question = Question.objects.create(desc='Test question')
        voting = Voting.objects.create(name='Test Voting', question=question)
        preference = Preference.objects.create(voting_id=voting.id)

        # Asegurarse de que la excepción se genera correctamente
        with self.assertRaises(ValidationError) as context:
            preference.sort(voting)

        # Verificar que el mensaje de error esperado está presente en la excepción generada
        expected_error_message = 'No postprocessing data available.'
        self.assertIn(expected_error_message, str(context.exception))


    def test_dhondt_method_no_postproc(self):
        # Crear objetos de prueba
        question = Question.objects.create(desc='Test question')
        voting = Voting.objects.create(name='Test Voting', question=question)
        apportionment = Apportionment.objects.create(voting_id=voting.id, seats=7)

        # Asegurarse de que la excepción se genera correctamente
        with self.assertRaises(ValidationError) as context:
            apportionment.dhondt(voting)

        # Verificar que el mensaje de error esperado está presente en la excepción generada
        expected_error_message = 'No postprocessing data available.'
        self.assertIn(expected_error_message, str(context.exception))


    def test_sainte_lague_method_no_postproc(self):
        # Crear objetos de prueba
        question = Question.objects.create(desc='Test question')
        voting = Voting.objects.create(name='Test Voting', question=question)
        apportionment = Apportionment.objects.create(voting_id=voting.id, seats=7)

        # Asegurarse de que la excepción se genera correctamente
        with self.assertRaises(ValidationError) as context:
            apportionment.sainte_lague(voting)

        # Verificar que el mensaje de error esperado está presente en la excepción generada
        expected_error_message = 'No postprocessing data available.'
        self.assertIn(expected_error_message, str(context.exception))