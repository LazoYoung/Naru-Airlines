import random
import string

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class LoginTest(TestCase):
    def test_incomplete_login_form(self):
        payload1 = {}
        payload2 = {'password': get_random_string(8)}
        payload3 = {'email': get_random_email()}
        response1 = self.client.post(reverse('rest_login'), data=payload1)
        response2 = self.client.post(reverse('rest_login'), data=payload2)
        response3 = self.client.post(reverse('rest_login'), data=payload3)
        self.assertTrue(status.is_client_error(response1.status_code))
        self.assertTrue(status.is_client_error(response2.status_code))
        self.assertTrue(status.is_client_error(response3.status_code))
        self.assertTrue('password' in response1.json())
        self.assertTrue('non_field_errors' in response2.json())
        self.assertTrue('password' in response3.json())

    def test_login_with_invalid_credentials(self):
        correct_email = get_random_email()
        correct_pwd = get_random_string(8)
        reg_response = post_registration(self.client, email=correct_email, password=correct_pwd)
        self.assertTrue(status.is_success(reg_response.status_code))

        invalid_email_cred = {'email': get_random_email(), 'password': correct_pwd}
        invalid_password_cred = {'email': correct_email, 'password': get_random_string(8)}
        response1 = self.client.post(reverse('rest_login'), data=invalid_email_cred)
        response2 = self.client.post(reverse('rest_login'), data=invalid_password_cred)
        self.assertTrue('non_field_errors' in response1.json())
        self.assertTrue('non_field_errors' in response2.json())

    def test_login_with_valid_credentials(self):
        email = get_random_email()
        pwd = get_random_string(8)
        register = post_registration(self.client, email=email, password=pwd)
        self.assertTrue(status.is_success(register.status_code))

        login = self.client.post(reverse('rest_login'), data={'email': email, 'password': pwd})
        self.assertTrue(status.is_success(login.status_code))


class LogoutTest(TestCase):
    def test_logout(self):
        self.client.login()
        response = self.client.post(reverse('rest_logout'))
        self.assertTrue(status.is_success(response.status_code))


class PasswordChangeTest(TestCase):
    def test_password_change_with_old_password_mismatch(self):
        register = post_registration(self.client, email=get_random_email(), password=get_random_string(8))
        self.assertTrue(status.is_success(register.status_code))

        new_password = get_random_string(8)
        change = self.client.post(reverse('rest_password_change'), data={
            'new_password1': new_password,
            'new_password2': new_password,
            'old_password': get_random_string(8)
        })
        self.assertTrue(status.is_client_error(change.status_code))

    def test_password_change_with_new_password_mismatch(self):
        old_password = get_random_string(8)
        register = post_registration(self.client, email=get_random_email(), password=old_password)
        self.assertTrue(status.is_success(register.status_code))

        change = self.client.post(reverse('rest_password_change'), data={
            'new_password1': get_random_string(8),
            'new_password2': get_random_string(8),
            'old_password': old_password
        })
        self.assertTrue(status.is_client_error(change.status_code))

    def test_password_change(self):
        old_password = get_random_string(8)
        register = post_registration(self.client, email=get_random_email(), password=old_password)
        self.assertTrue(status.is_success(register.status_code))

        new_password = get_random_string(8)
        change = self.client.post(reverse('rest_password_change'), data={
            'new_password1': new_password,
            'new_password2': new_password,
            'old_password': old_password
        })
        self.assertTrue(status.is_success(change.status_code))


class PasswordResetTest(TestCase):
    def test_password_reset(self):
        email = get_random_email()
        password = get_random_string(8)
        register = post_registration(self.client, email=email, password=password)
        self.assertTrue(status.is_success(register.status_code))

        self.client.login(email=email, password=password)
        reset = self.client.post(reverse('rest_password_reset'), data={
            'email': email
        })
        self.assertTrue(status.is_success(reset.status_code))


class RegisterTest(TestCase):
    def test_register_with_handle(self):
        email = get_random_email()
        pwd = get_random_string(8)
        response = self.client.post(reverse('rest_register'), data={
            'email': email,
            'username': get_random_string(8),
            'password1': pwd,
            'password2': pwd,
        })
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertTrue('username' in response.json())

    def test_register_with_incomplete_form(self):
        response1 = post_registration(self.client, email='', password=get_random_string(8))
        response2 = post_registration(self.client, email=get_random_email(), password='')
        self.assertTrue(status.is_client_error(response1.status_code))
        self.assertTrue(status.is_client_error(response2.status_code))
        self.assertTrue('email' in response1.json())
        self.assertTrue('password1' in response2.json())

    def test_register_with_duplicate_email(self):
        duplicate_email = get_random_email()
        response1 = post_registration(self.client, email=duplicate_email, password=get_random_string(8))
        response2 = post_registration(self.client, email=duplicate_email, password=get_random_string(8))
        self.assertTrue(status.is_success(response1.status_code))
        self.assertTrue(status.is_client_error(response2.status_code))

    def test_register_with_complete_form(self):
        response = post_registration(self.client, email=get_random_email(), password=get_random_string(8))
        self.assertTrue(status.is_success(response.status_code))


def get_random_string(length, lowercase=False):
    seq = string.ascii_lowercase + string.digits if lowercase else string.ascii_letters + string.digits
    return ''.join(random.choice(seq) for _ in range(length))


def get_random_email():
    return get_random_string(12, lowercase=True) + "@mailtest.org"


def post_registration(client, email=None, password=None):
    if email is None:
        email = get_random_email()

    if password is None:
        password = get_random_string(10)

    form = {'email': email, 'password1': password, 'password2': password}
    response = client.post(reverse('rest_register'), data=form)
    return response
