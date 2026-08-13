from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from ..models import Task
from .serializers import TaskDetailSerializer, TaskCreateSerializer, TaskUpdateSerializer
from .permissions import IsBoardMember



class AssignedTasksView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        tasks=Task.objects.filter(
            assignee=request.user
            )

        serializer=TaskDetailSerializer(tasks, many=True)

        return Response(serializer.data)



class ReviewingTasksView(APIView):
    permission_classes=[IsAuthenticated]


    def get(self, request):
        tasks=Task.objects.filter(reviewer=request.user)

        serializer=TaskDetailSerializer(tasks, many=True)

        return Response(serializer.data)



class TaskListView(APIView):
    permission_classes=[IsAuthenticated, IsBoardMember]

    def post(self, request):
        serializer=TaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            task=serializer.save()
            response_serializer=TaskDetailSerializer(task)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )



class TaskDetailView(APIView):
    permission_classes=[IsAuthenticated, IsBoardMember]

    def patch(self, request, task_id):
        task=Task.objects.filter(id=task_id).first()

        if task is None:
            return Response(
                {"detail":"Task not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer=TaskUpdateSerializer(
            task,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            response_serializer=TaskDetailSerializer(serializer.instance)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, task_id):
        task=Task.objects.filter(id=task_id).first()

        if task is None:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)