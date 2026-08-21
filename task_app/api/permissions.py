from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound

from board_app.models import Board
from task_app.models import Task


class IsBoardMember(BasePermission):
    """Allow access only to users who are members of the relevant board."""

    def has_permission(self, request, view):
        """Check whether the user is a member of the requested board."""
        task_id = view.kwargs.get('task_id')

        if task_id:
            return self._is_task_member(request, task_id)

        return self._is_board_member(request)

    def _is_board_member(self, request):
        """Check whether the user belongs to the board in the request data."""
        board_id = request.data.get('board')

        if not board_id:
            return False

        board = Board.objects.filter(id=board_id).first()

        if board is None:
            raise NotFound("Board not found...")

        return board.members.filter(
            id=request.user.id
        ).exists()

    def _is_task_member(self, request, task_id):
        """Check whether the user belongs to the board of the given task."""
        task = Task.objects.filter(id=task_id).first()

        if task is None:
            return True

        return task.board.members.filter(
            id=request.user.id
        ).exists()
