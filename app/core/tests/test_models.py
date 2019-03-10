from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful """
        email = 'test@example.com'
        password = 'Testpass123'
        # Use get_user_model() to refer to User instead of referring
        # to User directly. Otherwise your code will not work in 
        # projects where the AUTH_USER_MODEL setting has been changed
        # to a different user model
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """ Test the email for a new user is normalized """
        email = 'test@EXAMPLE.COM'
        user = get_user_model().objects.create_user(
            email=email, password='test123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        # it means assert will raise an exception if ValueError is not raised
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """ Test creating a new superuser """
        user = get_user_model().objects.create_superuser(
            email="test.example.com",
            password="test123"
        )

        # field is part of the PermissionsMixin
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)