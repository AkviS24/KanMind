from django.test import TestCase
from rest_framework.test import APIClient

from auth_app.models import User
from board_app.models import Board


class BoardViewsTest(TestCase):

    def setUp(self):
        self.client=APIClient()

        self.owner=User.objects.create_user(
            email='owner@test.com',
            password='password123',
            fullname='Board Owner',
        )

        self.member=User.objects.create_user(
            email='member@test.com',
            password='password123',
            fullname='Board Member',
        )

        self.board=Board.objects.create(
            title='Test Board',
            owner=self.owner,
        )

    def test_list_boards_returns_owned_boards(self):
        self.client.force_authenticate(
            user=self.owner
        )

        response=self.client.get('/api/boards/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['title'],
            'Test Board',
        )



    def test_list_boards_returns_member_boards(self):
        self.board.members.add(self.member)

        self.client.force_authenticate(
            user=self.member
        )

        response=self.client.get('/api/boards/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['title'],
            'Test Board',
        )



    def test_create_board_success(self):
        self.client.force_authenticate(
            user=self.owner
        )

        data={
            'title': 'New Board',
        }

        response=self.client.post(
            '/api/boards/',
            data,
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data['title'],
            'New Board',
        )
        self.assertEqual(
            response.data['owner_id'],
            self.owner.id,
        )

        self.assertTrue(
            Board.objects.filter(
                title='New Board',
                owner=self.owner,
            ).exists()
        )



    def test_create_board_invalid_data(self):
        self.client.force_authenticate(
            user=self.owner
        )

        response=self.client.post(
            '/api/boards/',
            {},
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.data)



    def test_get_board_details_as_owner(self):
        self.client.force_authenticate(
            user=self.owner
        )

        response=self.client.get(
            f'/api/boards/{self.board.id}/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['id'],
            self.board.id,
        )
        self.assertEqual(
            response.data['title'],
            'Test Board',
        )
        self.assertEqual(
            response.data['owner_id'],
            self.owner.id,
        )



    def test_get_board_details_as_member(self):
        self.board.members.add(self.member)

        self.client.force_authenticate(
            user=self.member
        )

        response=self.client.get(
            f'/api/boards/{self.board.id}/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['id'],
            self.board.id,
        )
        self.assertEqual(
            response.data['title'],
            'Test Board',
        )



    def test_get_board_not_found(self):
        self.client.force_authenticate(
            user=self.owner
        )

        response=self.client.get(
            '/api/boards/99999/'
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data['detail'],
            'Board not found',
        )



    def test_update_board_success(self):
        self.client.force_authenticate(
            user=self.owner
        )

        data={
            'title': 'Updated Board',
        }

        response=self.client.patch(
            f'/api/boards/{self.board.id}/',
            data,
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['title'],
            'Updated Board',
        )

        self.board.refresh_from_db()

        self.assertEqual(
            self.board.title,
            'Updated Board',
        )



    def test_update_board_invalid_data(self):
        self.client.force_authenticate(
            user=self.owner
        )

        data={
            'title': 'A' * 151,
        }

        response=self.client.patch(
            f'/api/boards/{self.board.id}/',
            data,
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.data)



    def test_update_board_not_found(self):
        self.client.force_authenticate(
            user=self.owner
        )

        data={
            'title': 'Updated Board',
        }

        response=self.client.patch(
            '/api/boards/99999/',
            data,
            format='json',
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data['detail'],
            'Board not found',
        )



    def test_delete_board_success(self):
        self.client.force_authenticate(
            user=self.owner
        )

        board_id=self.board.id

        response=self.client.delete(
            f'/api/boards/{board_id}/'
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Board.objects.filter(id=board_id).exists()
        )



    def test_delete_board_not_found(self):
        self.client.force_authenticate(
            user=self.owner
        )

        response=self.client.delete(
            '/api/boards/99999/'
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data['detail'],
            'Board not found',
        )



    def test_delete_board_permission_denied(self):
        self.client.force_authenticate(
            user=self.member
        )

        response=self.client.delete(
            f'/api/boards/{self.board.id}/'
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data['detail'],
            'Permission denied',
        )

        self.assertTrue(
            Board.objects.filter(
                id=self.board.id
            ).exists()
        )