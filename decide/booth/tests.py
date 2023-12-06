from django.test import TestCase
from base.tests import BaseTestCase
from http import HTTPStatus


# Create your tests here.

class BoothTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
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
        self.assertContains(response, "<h1>Registra un nuevo usuario</h1>", html=True)

   # def test_post_success(self):
    #    response = self.client.post("/booth/register/", data={"username": "Menganito"})

     #   self.assertEqual(response.status_code, HTTPStatus.FOUND)
      #  self.assertEqual(response["Location"], "/books/")

    def test_post_error(self):
        response = self.client.post("/booth/register/", data={"username": " "})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Username no puede estar vacio", html=True)
       