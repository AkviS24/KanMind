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
    """Provide tasks assigned to the authenticated user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return all tasks assigned to the current user."""
        tasks = Task.objects.filter(assignee=request.user)
        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data)


class ReviewingTasksView(APIView):
    """Provide tasks that the authenticated user has to review."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return all tasks assigned to the current user for review."""
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskListView(APIView):
    """Handle task creation for board members."""

    permission_classes = [IsAuthenticated, IsBoardMember]

    def post(self, request):
        """Create a new task for a board."""
        serializer = TaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            task = serializer.save(creator=request.user)
            return self._success_response(task)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _success_response(self, task):
        """Return the serialized task after successful creation."""
        serializer = TaskDetailSerializer(task)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class TaskDetailView(APIView):
    """Handle retrieving, updating, and deleting individual tasks."""

    permission_classes = [IsAuthenticated, IsBoardMember]

    def get(self, request, task_id):
        """Return details of the requested task."""
        task = self._get_task(task_id)

        if task is None:
            return self._not_found()

        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)

    def patch(self, request, task_id):
        """Update the requested task with the provided data."""
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
        """Delete a task if the user is its creator or board owner."""
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
        """Return the task with the given ID or None if it does not exist."""
        return Task.objects.filter(id=task_id).first()

    def _not_found(self):
        """Return the standard response for a missing task."""
        return Response(
            {"detail": "Task not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    def _update_response(self, task):
        """Return the updated task as serialized response data."""
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)


class CommentsView(APIView):
    """Handle comments belonging to a specific task."""

    permission_classes = [IsAuthenticated, IsBoardMember]

    def get(self, request, task_id):
        """Return all comments belonging to the requested task."""
        task = self._get_task(task_id)

        if task is None:
            return self._not_found()

        comments = task.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, task_id):
        """Create a new comment for the requested task."""
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
        """Delete a comment if the authenticated user is its author."""
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
        """Return the task with the given ID or None if it does not exist."""
        return Task.objects.filter(id=task_id).first()

    def _not_found(self):
        """Return the standard response for a missing task."""
        return Response(
            {"detail": "Task not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    def _create_comment(self, serializer, task, user):
        """Save and return a new comment for the specified task."""
        comment = serializer.save(task=task, author=user)
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )
