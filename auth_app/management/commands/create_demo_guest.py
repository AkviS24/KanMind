import os

from django.core.management.base import BaseCommand, CommandError

from auth_app.models import User
from board_app.models import Board
from task_app.models import Task


def get_guest_credentials():
    """Return the configured demo guest credentials."""
    email = os.getenv("KANMIND_GUEST_EMAIL")
    password = os.getenv("KANMIND_GUEST_PASSWORD")
    if not email or not password:
        raise CommandError(
            "Set KANMIND_GUEST_EMAIL and KANMIND_GUEST_PASSWORD."
        )
    return email, password


def create_guest_user(email, password):
    """Create or update the dedicated demo guest account."""
    fullname = os.getenv("KANMIND_GUEST_FULLNAME", "KanMind Guest")
    user, _ = User.objects.get_or_create(
        email=email,
        defaults={"fullname": fullname},
    )
    user.fullname = fullname
    user.is_active = True
    user.is_staff = False
    user.is_superuser = False
    user.set_password(password)
    user.save()
    return user


def create_demo_board(user):
    """Create the sample board and make the guest its member."""
    board, _ = Board.objects.get_or_create(
        title="KanMind Demo Board",
        owner=user,
    )
    board.members.add(user)
    return board


def create_demo_tasks(board, user):
    """Create sample tasks without duplicating existing demo data."""
    samples = [
        (
            "Plan the project",
            "Collect the first ideas and define the next steps.",
            "to-do",
            "high",
        ),
        (
            "Create the first task",
            "Try changing the status and priority.",
            "in-progress",
            "medium",
        ),
        (
            "Review the KanMind board",
            "Open this task and add a comment.",
            "review",
            "low",
        ),
    ]
    for title, description, status, priority in samples:
        Task.objects.get_or_create(
            board=board,
            title=title,
            defaults={
                "creator": user,
                "assignee": user,
                "reviewer": user,
                "description": description,
                "status": status,
                "priority": priority,
            },
        )


class Command(BaseCommand):
    """Prepare the isolated database for the public KanMind demo."""

    help = "Create the demo guest account and sample board."

    def handle(self, *args, **options):
        """Create the demo user and its initial sample data."""
        email, password = get_guest_credentials()
        guest = create_guest_user(email, password)
        board = create_demo_board(guest)
        create_demo_tasks(board, guest)
        self.stdout.write(self.style.SUCCESS(f"Demo guest ready: {email}"))
