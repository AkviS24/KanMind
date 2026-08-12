from django.db.models import Q
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