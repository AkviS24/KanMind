from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Board
from .serializers import BoardDetailSerializer, BoardSerializer, BoardUpdateSerializer


class BoardListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(
            Q(owner=request.user) | Q(members=request.user)
        ).distinct()

        serializer = BoardSerializer(boards, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED,)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,)


class BoardDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        board = Board.objects.filter(id=board_id).first()

        if board is None:
            return Response(
                {"detail": "Board not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if board.owner != request.user and not board.members.filter(
            id=request.user.id
        ).exists():
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = BoardDetailSerializer(board)

        return Response(serializer.data)

    def patch(self, request, board_id):
        board = Board.objects.filter(id=board_id).first()

        if board is None:
            return Response(
                {"detail": "Board not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if board.owner != request.user and not board.members.filter(
            id=request.user.id
        ).exists():
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = BoardUpdateSerializer(
            board,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            response_serializer = BoardDetailSerializer(serializer.instance)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, board_id):
        board = Board.objects.filter(id=board_id).first()

        if board is None:
            return Response(
                {"detail": "Board not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if board.owner != request.user:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        board.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)