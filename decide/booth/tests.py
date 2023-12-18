from django.urls import reverse
from base.tests import BaseTestCase
from http import HTTPStatus
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY

# Create your tests here.

class BoothTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser', email='testuser@email.com', password='testpassword')
        self.superuser = User.objects.create_superuser(username='superuser', email='superuser@example.com', password='superpassword')
    def tearDown(self):
        super().tearDown()
    def testBoothNotFound(self):

        # Se va a probar con el numero 10000 pues en las condiciones actuales en las que nos encontramos no parece posible que se genren 10000 votaciones diferentes
        response = self.client.get('/booth/10000/')
        self.assertEqual(response.status_code, 404)

    def testBoothRedirection(self):

        # Se va a probar con el numero 10000 pues en las condiciones actuales en las que nos encontramos no parece posible que se genren 10000 votaciones diferentes
        response = self.client.get('/booth/10000')
        self.assertEqual(response.status_code, 301)

    def test_get(self):
        response = self.client.get("/booth/register/")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "REGISTRO DE USUARIO")

    def test_post_success(self):
        response = self.client.post("/booth/register/", data={
            'username': 'EGCuser1',
            'email': 'egcuser1@email.com',
            'password1': 'EGCenjoyer1',
            'password2': 'EGCenjoyer1'
        })

        self.assertEqual(response["Location"], "/booth/thanks/")

    def test_forms(self):
        form_test = CreateUserForm(data={
            'username': 'EGCuser1',
            'email': 'egcuser1@email.com',
            'password1': 'EGCenjoyer1',
            'password2': 'EGCenjoyer1'
        })
        self.assertTrue(form_test.is_valid())

    def test_forms_empty(self):
        form_test = CreateUserForm(data={})
        self.assertFalse(form_test.is_valid())

    def test_forms_wrong(self):
        form_test = CreateUserForm(data = {
            'username': 'EGCuser2',
            'email': 'egcuser2@email.com',
            'password1': 'EGCenjoyer1',
            'password2': 'olvidelapassword'
        })
        self.assertFalse(form_test.is_valid())

    def test_login_successful(self):
        # Prueba de inicio de sesión exitoso con credenciales válidas
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        expected_url = reverse('home')
        self.assertEqual(response.status_code, 302)  # 302: Redirección al inicio de sesión exitoso
        self.assertRedirects(response, expected_url)

    def test_login_email_successful(self):
        # Prueba de inicio de sesión exitoso con credenciales válidas
        url = reverse('login')
        data = {'username': 'testuser@email.com', 'password': 'testpassword'}
        response = self.client.post(url, data)
        expected_url = reverse('home')
        self.assertEqual(response.status_code, 302)  # 302: Redirección al inicio de sesión exitoso
        self.assertRedirects(response, expected_url)

    def test_login_unsuccessful(self):
        # Prueba de inicio de sesión fallido con credenciales inválidas
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # 200: Página de inicio de sesión (fallido)
        self.assertContains(response, 'Nombre de usuario/correo electrónico o contraseña incorrectos')

    def test_login_email_unsuccessful(self):
        # Prueba de inicio de sesión fallido con credenciales inválidas
        url = reverse('login')
        data = {'username': 'emailincorrecto@email.com', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # 200: Página de inicio de sesión (fallido)
        self.assertContains(response, 'Nombre de usuario/correo electrónico o contraseña incorrectos')

    def test_logout(self):
        # Iniciar sesión primero para realizar el cierre de sesión
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)

        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # 302: Redirección al cierre de sesión

        # Verificar que la clave de sesión ya no esté presente
        session_key = self.client.session.get(SESSION_KEY)
        self.assertIsNone(session_key)

    def test_login_superuser_redirect(self):
        # Prueba de inicio de sesión exitoso para superusuario
        url = reverse('login')
        data = {'username': 'superuser', 'password': 'superpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirección al éxito de inicio de sesión
        self.assertRedirects(response, '/admin', fetch_redirect_response=False)

    def test_home_page_no_votes(self):

        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['my_votings'], [])

    def test_get_change_user_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('change_user'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_user.html')

    def test_change_user_valid_form(self):
        self.client.force_login(self.user)
        data = {'username': 'newusername', 'email': 'new@example.com'}
        response = self.client.post(reverse('change_user'), data)

        self.assertRedirects(response, reverse('home'))  # Verifica la redirección después de guardar

    def test_change_user_invalid_form(self):
        self.client.force_login(self.user)
        data = {}  # Envía un formulario vacío
        response = self.client.post(reverse('change_user'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'Este campo es requerido.')  # Verifica el error en el formulario