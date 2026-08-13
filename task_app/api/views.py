from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Task, Comment
from .permissions import IsBoardMember
from .serializers import (
    TaskDetailSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    CommentSerializer,
)


class AssignedTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assignee=request.user)
        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data)


class ReviewingTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskListView(APIView):
    permission_classes = [IsAuthenticated, IsBoardMember]

    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            task = serializer.save(creator=request.user)
            return self._success_response(task)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _success_response(self, task):
        serializer = TaskDetailSerializer(task)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get(self, request, task_id):
        task = self._get_task(task_id)

        if task is None:
            return self._not_found()

        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)

    def patch(self, request, task_id):
        task = self._get_task(task_id)

        if task is None:
            return self._not_found()

        serializer = TaskUpdateSerializer(
            task,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return self._update_response(serializer.instance)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, task_id):
        task = self._get_task(task_id)

        if task is None:
            return self._not_found()

        if request.user != task.creator and request.user != task.board.owner:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_task(self, task_id):
        return Task.objects.filter(id=task_id).first()

    def _not_found(self):
        return Response(
            {"detail": "Task not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    def _update_response(self, task):
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)


class CommentsView(APIView):
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get(self, request, task_id):
        task = self._get_task(task_id)

        if task is None:
            return self._not_found()

        comments = task.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, task_id):
        task = self._get_task(task_id)

        if task is None:
            return self._not_found()

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            return self._create_comment(serializer, task, request.user)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, task_id, comment_id):
        comment = Comment.objects.filter(
            id=comment_id,
            task_id=task_id,
        ).first()

        if comment is None:
            return Response(
                {"detail": "Comment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if comment.author != request.user:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_task(self, task_id):
        return Task.objects.filter(id=task_id).first()

    def _not_found(self):
        return Response(
            {"detail": "Task not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    def _create_comment(self, serializer, task, user):
        comment = serializer.save(task=task, author=user)
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )
