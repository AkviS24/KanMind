from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Board
from .serializers import BoardSerializer

class BoardListView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        boards=Board.objects.filter(
            Q(owner=request.user) | Q(members=request.user)
        ).distinct()

        serializer=BoardSerializer(boards, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer=BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED,)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,)