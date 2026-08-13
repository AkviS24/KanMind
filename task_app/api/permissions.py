from rest_framework.permissions import BasePermission

from board_app.models import Board
from task_app.models import Task


class IsBoardMember(BasePermission):

    def has_permission(self, request, view):
        task_id=view.kwargs.get('task_id')

        if task_id:
            return self._is_task_member(request, task_id)

        return self._is_board_member(request)

    def _is_board_member(self, request):
        board_id=request.data.get('board')

        if not board_id:
            return False

        return Board.objects.filter(
            id=board_id,
            members=request.user,
        ).exists()


    def _is_task_member(self, request, task_id):
        task=Task.objects.filter(id=task_id).first()

        if task is None:
            return True

        return task.board.members.filter(
            id=request.user.id
        ).exists()



class IsTaskCreatorOrBoardOwner(BasePermission):

    def has_permission(self, request, view):
        task_id = view.kwargs.get('task_id')

        if not task_id:
            return False

        task = Task.objects.filter(id=task_id).first()

        if task is None:
            return True

        return (
            task.creator_id == request.user.id
            or task.board.owner_id == request.user.id
        )