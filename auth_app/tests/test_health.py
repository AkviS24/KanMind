from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase, override_settings

from rest_framework import status

from core.health import health_check


@override_settings(SECURE_SSL_REDIRECT=False)
class HealthCheckTests(TestCase):
    """Test the private application readiness endpoint."""

    def test_health_check_returns_ok_when_database_is_available(self):
        """Report readiness when the database accepts a query."""

        response = self.client.get("/internal/health/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok"})

    @patch(
        "core.health.connection.cursor",
        side_effect=DatabaseError("Database unavailable"),
    )
    def test_health_check_returns_service_unavailable(self, mock_cursor):
        """Do not report readiness when the database is unavailable."""

        response = self.client.get("/internal/health/")

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )
        self.assertEqual(response.json(), {"status": "unavailable"})
        mock_cursor.assert_called_once()

    def test_health_check_rejects_post_requests(self):
        """Keep the readiness endpoint read-only."""

        response = self.client.post("/internal/health/")

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
