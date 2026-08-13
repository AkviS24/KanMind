from rest_framework.permissions import BasePermission

from board_app.models import Board
from task_app.models import Task


class IsBoardMember(BasePermission):

    def has_permission(self, request, view):
        if view.__class__.__name__ == 'TaskDetailView':
            return self._is_task_member(request, view)

        board_id=request.data.get('board')

        if not board_id:
            return False

        return Board.objects.filter(
            id=board_id,
            members=request.user,
        ).exists()


    def _is_task_member(self, request, view):
        task_id=view.kwargs.get('task_id')

        return Task.objects.filter(
            id=task_id,
            board__members=request.user,
        ).exists()