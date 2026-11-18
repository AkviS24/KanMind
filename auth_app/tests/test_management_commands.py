import os
from unittest.mock import patch

from django.core.management import call_command, CommandError
from django.test import TestCase

from auth_app.models import User
from board_app.models import Board
from task_app.models import Task


class CreateDemoGuestCommandTests(TestCase):
    """Test provisioning of the isolated demo guest account."""

    @patch.dict(os.environ, {}, clear=True)
    def test_command_requires_guest_credentials(self):
        """Reject startup when the demo credentials are missing."""
        with self.assertRaises(CommandError):
            call_command("create_demo_guest")

    @patch.dict(os.environ, {
        "KANMIND_GUEST_EMAIL": "guest@example.com",
        "KANMIND_GUEST_PASSWORD": "demo-password-123",
    })
    def test_command_creates_guest_and_sample_data(self):
        """Create the guest account, board, and sample tasks."""
        call_command("create_demo_guest")
        guest = User.objects.get(email="guest@example.com")
        board = Board.objects.get(owner=guest, title="KanMind Demo Board")
        self.assertTrue(guest.check_password("demo-password-123"))
        self.assertIn(guest, board.members.all())
        self.assertEqual(Task.objects.filter(board=board).count(), 3)

    @patch.dict(os.environ, {
        "KANMIND_GUEST_EMAIL": "guest@example.com",
        "KANMIND_GUEST_PASSWORD": "demo-password-123",
    })
    def test_command_can_run_more_than_once(self):
        """Keep the sample board and tasks unique across restarts."""
        call_command("create_demo_guest")
        call_command("create_demo_guest")
        guest = User.objects.get(email="guest@example.com")
        board = Board.objects.get(owner=guest, title="KanMind Demo Board")
        self.assertEqual(Board.objects.filter(owner=guest).count(), 1)
        self.assertEqual(Task.objects.filter(board=board).count(), 3)
