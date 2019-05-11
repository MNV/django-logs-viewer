from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model

from log import models as LogModels


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@test.test'
        password = 'secret123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_new_user_email_normalized(self):
        """ Test the email is normalized"""
        email = 'test@TEST.TeSt'
        user = get_user_model().objects.create_user(email, 'secret123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'secret123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@test.test',
            'secret123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_log_str(self):
        """Test the log string representation"""
        log = LogModels.Log.objects.create(
            time=timezone.now(),
            level='warning',
            message='Warning message body',
            details={
                'kwargs': {'k1': 'v1', 'k2': 'v2'},
                'exec_time': timezone.now().isoformat(),
                'traceback': ['line1', 'line2'],
            }
        )

        self.assertEqual(str(log), log.level)
