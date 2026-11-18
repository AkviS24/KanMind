from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from auth_app.models import User


class RegistrationEndpointDisabledTest(TestCase):
    """Ensure public account creation is no longer exposed."""

    def setUp(self):
        self.client = APIClient()

    def test_registration_endpoint_returns_not_found(self):
        response = self.client.post(
            "/api/registration/",
            {
                "fullname": "Unexpected User",
                "email": "unexpected@test.com",
                "password": "password123",
                "repeated_password": "password123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(User.objects.filter(email="unexpected@test.com").exists())


class LoginViewTest(TestCase):

    def setUp(self):
        self.client=APIClient()

        self.user=User.objects.create_user(
            email='login-view@test.com',
            password='password123',
            fullname='Login View User',
        )

    def test_login_success(self):
        data={
            'email': 'login-view@test.com',
            'password': 'password123',
        }

        response=self.client.post(
            '/api/login/',
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            response.data['email'],
            'login-view@test.com',
        )
        self.assertEqual(
            response.data['fullname'],
            'Login View User',
        )
        self.assertIn(
            'token',
            response.data,
        )
        self.assertTrue(
            Token.objects.filter(
                user=self.user,
            ).exists()
        )


    def test_login_invalid_password(self):
        data={
            'email': 'login-view@test.com',
            'password': 'wrongpassword',
        }

        response=self.client.post(
            '/api/login/',
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            400,
        )
        self.assertIn(
            'non_field_errors',
            response.data,
        )

    def test_login_with_existing_token(self):
        Token.objects.create(user=self.user)

        data = {
            'email': 'login-view@test.com',
            'password': 'password123',
        }

        response = self.client.post(
            '/api/login/',
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertIn(
            'token',
            response.data,
        )


class LoginPolicyTest(TestCase):
    """Test the production and demo authentication restrictions."""

    def setUp(self):
        self.client = APIClient()
        self.demo_user = User.objects.create_user(
            email="demo-policy@test.com",
            password="password123",
            fullname="Demo Policy User",
        )
        self.other_user = User.objects.create_user(
            email="other-policy@test.com",
            password="password123",
            fullname="Other Policy User",
        )

    @override_settings(KANMIND_LOGIN_DISABLED=True)
    def test_login_is_disabled_on_production_backend(self):
        response = self.client.post(
            "/api/login/",
            {"email": self.demo_user.email, "password": "password123"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    @override_settings(
        KANMIND_GUEST_ONLY_LOGIN=True,
        KANMIND_GUEST_EMAIL="demo-policy@test.com",
    )
    def test_demo_backend_rejects_non_demo_accounts(self):
        response = self.client.post(
            "/api/login/",
            {"email": self.other_user.email, "password": "password123"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    @override_settings(
        KANMIND_GUEST_ONLY_LOGIN=True,
        KANMIND_GUEST_EMAIL="demo-policy@test.com",
    )
    def test_demo_backend_accepts_configured_demo_account(self):
        response = self.client.post(
            "/api/login/",
            {"email": self.demo_user.email, "password": "password123"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.demo_user.email)


class EmailCheckViewTest(TestCase):

    def setUp(self):
        self.client=APIClient()

    def test_email_check_unauthenticated(self):
        response=self.client.get(
            '/api/email-check/',
            {'email': 'test@test.com'},
        )

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_email_check_valid(self):
        user=User.objects.create_user(
            email='email-check@test.com',
            password='password123',
            fullname='Email Check User',
        )

        self.client.force_authenticate(user=user)

        response=self.client.get(
            '/api/email-check/',
            {'email': 'email-check@test.com'},
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            response.data,
            {
                'id': user.id,
                'email': 'email-check@test.com',
                'fullname': 'Email Check User',
            },
        )

    def test_email_check_invalid_email(self):
        user=User.objects.create_user(
            email='email-check@test.com',
            password='password123',
            fullname='Email Check User',
        )

        self.client.force_authenticate(user=user)

        response=self.client.get(
            '/api/email-check/',
            {'email': 'not-an-email'},
        )

        self.assertEqual(
            response.status_code,
            400,
        )
        self.assertIn(
            'email',
            response.data,
        )

    def test_email_check_user_not_found(self):
        user=User.objects.create_user(
            email='existing@test.com',
            password='password123',
            fullname='Existing User',
        )

        self.client.force_authenticate(user=user)

        response=self.client.get(
            '/api/email-check/',
            {'email': 'unknown@test.com'},
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_email_check_missing_email(self):
        user = User.objects.create_user(
            email='email-check@test.com',
            password='password123',
            fullname='Email Check User',
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(
            '/api/email-check/',
        )

        self.assertEqual(
            response.status_code,
            400,
        )
        self.assertIn(
            'email',
            response.data,
        )
