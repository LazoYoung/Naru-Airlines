import random

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.settings import api_settings

from .models import Member
from .utils import get_random_email, get_random_password, get_random_string


class RegisterTest(TestCase):
    def test_register_with_incomplete_form(self):
        response1 = post_register(
            self.client, display_name='', email=get_random_email(), password=get_random_password()
        )
        response2 = post_register(
            self.client, email='', password=get_random_password()
        )
        response3 = post_register(
            self.client, email=get_random_email(), password=''
        )
        self.assertTrue(status.is_client_error(response1.status_code))
        self.assertTrue(status.is_client_error(response2.status_code))
        self.assertTrue(status.is_client_error(response3.status_code))
        self.assertTrue('display_name' in response1.json())
        self.assertTrue('email' in response2.json())
        self.assertTrue('password' in response3.json())

    def test_register_with_duplicate_email(self):
        duplicate_email = get_random_email()
        response1 = post_register(self.client, email=duplicate_email, password=get_random_password())
        response2 = post_register(self.client, email=duplicate_email, password=get_random_password())
        self.assertTrue(status.is_success(response1.status_code))
        self.assertTrue(status.is_client_error(response2.status_code))

    def test_register_with_complete_form(self):
        response = post_register(self.client, email=get_random_email(), password=get_random_password())
        self.assertTrue(status.is_success(response.status_code))


class LoginTest(TestCase):
    def test_login_with_incomplete_form(self):
        payload1 = {}
        payload2 = {'password': get_random_password()}
        payload3 = {'email': get_random_email()}
        response1 = self.client.post(reverse('login'), data=payload1)
        response2 = self.client.post(reverse('login'), data=payload2)
        response3 = self.client.post(reverse('login'), data=payload3)
        self.assertTrue(status.is_client_error(response1.status_code))
        self.assertTrue(status.is_client_error(response2.status_code))
        self.assertTrue(status.is_client_error(response3.status_code))
        self.assertTrue('email' and 'password' in response1.json())
        self.assertTrue('email' in response2.json())
        self.assertTrue('password' in response3.json())

    def test_login_with_invalid_credentials(self):
        correct_email = get_random_email()
        correct_pwd = get_random_password()
        reg_response = post_register(self.client, email=correct_email, password=correct_pwd)
        self.assertTrue(status.is_success(reg_response.status_code))

        invalid_email_cred = {'email': get_random_email(), 'password': correct_pwd}
        invalid_password_cred = {'email': correct_email, 'password': get_random_password()}
        response1 = self.client.post(reverse('login'), data=invalid_email_cred)
        response2 = self.client.post(reverse('login'), data=invalid_password_cred)
        self.assertTrue(api_settings.NON_FIELD_ERRORS_KEY in response1.json())
        self.assertTrue(api_settings.NON_FIELD_ERRORS_KEY in response2.json())

    def test_login_with_valid_credentials(self):
        email = get_random_email()
        pwd = get_random_password()
        register = post_register(self.client, email=email, password=pwd)
        self.assertTrue(status.is_success(register.status_code))

        login = self.client.post(reverse('login'), data={'email': email, 'password': pwd})
        self.assertTrue(status.is_success(login.status_code))


class LogoutTest(TestCase):
    def test_logout(self):
        self.client.login()
        response = self.client.post(reverse('logout'))
        self.assertTrue(status.is_success(response.status_code))


class PasswordChangeTest(TestCase):
    def test_password_change_with_password_mismatch(self):
        old_password = get_random_password()
        register_and_login(self, password=old_password)

        new_password = get_random_password()
        change = self.client.post(reverse('change_password'), data={
            'old_password': get_random_password(),
            'new_password': new_password,
        })
        self.assertTrue(status.is_client_error(change.status_code))
        self.assertTrue('old_password' in change.json())

    def test_password_change_with_short_password(self):
        old_password = get_random_password()
        register_and_login(self, password=old_password)

        change = self.client.post(reverse('change_password'), data={
            'old_password': old_password,
            'new_password': get_random_password(length=5),
        })
        self.assertTrue(status.is_client_error(change.status_code))
        self.assertTrue('new_password' in change.json())

    def test_password_change(self):
        old_password = get_random_password()
        register_and_login(self, password=old_password)

        change = self.client.post(reverse('change_password'), data={
            'old_password': old_password,
            'new_password': get_random_password(),
        })
        self.assertTrue(status.is_success(change.status_code))


class PasswordResetTest(TestCase):
    def test_password_reset(self):
        email = get_random_email()
        password = get_random_password()
        register = post_register(self.client, email=email, password=password)
        self.assertTrue(status.is_success(register.status_code))

        self.client.login(email=email, password=password)
        reset = self.client.post(reverse('reset_password'), data={
            'email': email
        })
        self.assertTrue(status.is_success(reset.status_code))


class ProfileTest(TestCase):
    def test_unauthorized(self):
        get = self.client.get(reverse('profile'))
        put = self.client.put(reverse('profile'), data={})
        self.assertEqual(get.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(put.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_get(self):
        register_and_login(self)
        get = self.client.get(reverse('profile'))
        data = get.json()
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertTrue('handle' in data)
        self.assertTrue('display_name' in data)
        self.assertTrue('email' in data)
        self.assertTrue('is_verified' in data)

    def test_profile_put(self):
        register_and_login(self)
        display_name = "user-" + get_random_string(length=8)
        email = get_random_email()
        put = self.client.put(
            path=reverse('profile'),
            data={
                'display_name': display_name,
                'email': email,
            },
            content_type='application/json'
        )
        self.assertTrue(status.is_success(put.status_code))


def post_register(client, display_name=None, email=None, password=None, verify_email=True):
    if display_name is None:
        display_name = f"Dummy user #{random.randint(1, 100)}"

    if email is None:
        email = get_random_email()

    if password is None:
        password = get_random_password()

    form = {'display_name': display_name, 'email': email, 'password': password}
    response = client.post(reverse('register'), data=form)

    if verify_email and status.is_success(response.status_code):
        member = Member.objects.get(email__iexact=email)
        member.is_verified = True
        member.save()

    return response


def register_and_login(test_case: TestCase, display_name=None, email=None, password=None):
    if display_name is None:
        display_name = f"Dummy user #{random.randint(1, 100)}"

    if email is None:
        email = get_random_email()

    if password is None:
        password = get_random_password()

    register = post_register(
        test_case.client, display_name=display_name, email=email, password=password, verify_email=True
    )
    login = test_case.client.post(reverse('login'), data={
        'email': email,
        'password': password,
    })
    test_case.assertTrue(status.is_success(register.status_code))
    test_case.assertTrue(status.is_success(login.status_code))
