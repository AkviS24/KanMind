from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIClient


class AuthenticationThrottleTests(TestCase):
    """Test rate limits on public authentication endpoints."""

    def setUp(self):
        cache.clear()
        self.client = APIClient()

    def post_auth_request(self, path, payload):
        """Send an authentication request from a fixed client IP."""
        return self.client.post(
            path,
            payload,
            format="json",
            HTTP_X_FORWARDED_FOR="203.0.113.10",
        )

    def test_login_endpoint_is_rate_limited(self):
        """Limit repeated login attempts from the same client."""
        payload = {"email": "unknown@example.com", "password": "invalid"}
        for _ in range(10):
            response = self.post_auth_request("/api/login/", payload)
            self.assertEqual(response.status_code, 400)
        response = self.post_auth_request("/api/login/", payload)
        self.assertEqual(response.status_code, 429)

    def test_registration_endpoint_is_rate_limited(self):
        """Limit repeated account creation attempts from the same client."""
        for _ in range(5):
            response = self.post_auth_request("/api/registration/", {})
            self.assertEqual(response.status_code, 400)
        response = self.post_auth_request("/api/registration/", {})
        self.assertEqual(response.status_code, 429)
