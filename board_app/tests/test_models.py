from django.test import TestCase

from auth_app.models import User
from board_app.models import Board


class BoardModelTest(TestCase):

    def test_board_str_returns_title(self):
        user=User.objects.create_user(
            email='board-model@test.com',
            password='password123',
            fullname='Board Model User',
        )

        board=Board.objects.create(
            title='My Test Board',
            owner=user,
        )

        self.assertEqual(
            str(board),
            'My Test Board',
        )