from django.test import TestCase
from base.tests import BaseTestCase
from http import HTTPStatus
from .models import form
from .forms import OrderForm, CreateUserForm
from django.shortcuts import render, redirect

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
        self.assertContains(response, "<title>Registrar nuevo usuario</title>", html=True)

    def test_post_success(self):
        response = self.client.post("/booth/register/", data={
            'username': 'EGCuser1',
            'password1': 'EGCenjoyer1',
            'password2': 'EGCenjoyer1'
        })

        self.assertEqual(response["Location"], "/booth/thanks/")
    
    def test_forms(self):
        form_test = CreateUserForm(data={
            'username': 'EGCuser1',
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
            'password1': 'EGCenjoyer1',
            'password2': 'olvidelapassword'
        })
        self.assertFalse(form_test.is_valid())