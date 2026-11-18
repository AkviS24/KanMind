from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.test import APIClient


@override_settings(REST_FRAMEWORK={
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "login": "1/minute",
        "registration": "1/minute",
    },
})
class AuthenticationThrottleTests(TestCase):
    """Test rate limits on public authentication endpoints."""

    def setUp(self):
        cache.clear()
        self.client = APIClient()

    def test_login_endpoint_is_rate_limited(self):
        """Limit repeated login attempts from the same client."""
        payload = {"email": "unknown@example.com", "password": "invalid"}
        first = self.client.post("/api/login/", payload, format="json")
        second = self.client.post("/api/login/", payload, format="json")
        self.assertEqual(first.status_code, 400)
        self.assertEqual(second.status_code, 429)

    def test_registration_endpoint_is_rate_limited(self):
        """Limit repeated account creation attempts from the same client."""
        payload = {}
        first = self.client.post("/api/registration/", payload, format="json")
        second = self.client.post("/api/registration/", payload, format="json")
        self.assertEqual(first.status_code, 400)
        self.assertEqual(second.status_code, 429)
