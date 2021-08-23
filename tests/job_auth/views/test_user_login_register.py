from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from jobs_portal.job_auth.forms import RegisterForm

UserModel = get_user_model()


class TestUserRegister(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_registrationFormValid(self):
        user_form = RegisterForm({'email': 'test2@abv.bg',
                                  'username': 'test',
                                  'password1': 'test',
                                  'password2': 'test'})

        self.assertTrue(user_form.is_valid())

    def test_registrationFormInvalid(self):
        user_form = RegisterForm({'email': 'test2@abv.bg',
                                  'username': 'test',
                                  'password1': 'test',
                                  'password2': 'test12'})

        self.assertFalse(user_form.is_valid())

    def test_registrationFormInvalid_emailInvalid(self):
        user_form = RegisterForm({'email': 'test2.abv.bg',
                                  'username': 'test',
                                  'password1': 'test',
                                  'password2': 'test'})

        self.assertFalse(user_form.is_valid())

    def test_emailAlreadyExists(self):
        UserModel.objects.create_user(email='test2@abv.bg',
                                      username='test',
                                      password='test', )

        user_form = RegisterForm({'email': 'test2@abv.bg',
                                  'username': 'test',
                                  'password1': 'test',
                                  'password2': 'test'})

        self.assertFalse(user_form.is_valid())

    def test_userSubmitsTwoDifferentPasswords(self):
        response = self.client.post(reverse('register'), {'email': 'test2@abv.bg',
                                                          'username': 'test',
                                                          'password1': 'test',
                                                          'password2': 'test1'})

        self.assertNotIn('_auth_user_id', self.client.session)


class TestUserLogin(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = self.client.post(reverse('register'), data={
            'email': 'test2@abv.bg',
            'username': 'test',
            'password1': 'test',
            'password2': 'test',
        })

    def test_activationSuccess(self):
        self.user.is_active = True

        response = self.client.post(reverse('login'), data={'email': 'test2@abv.bg', 'password': 'test'})
        self.assertEqual(200, response.status_code)
