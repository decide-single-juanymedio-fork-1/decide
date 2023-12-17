from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from count.models import Preference, Apportionment
from voting.models import Voting, Question
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your tests here.

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