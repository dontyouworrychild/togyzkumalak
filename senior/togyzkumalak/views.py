from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import RegisterSerializer, ListUserDataSerializer, GameSessionSerializer, GameHistorySerializer
from django.contrib.auth.models import User
from .models import GameHistory, GameSession


class GameSessionViewsets(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer
    http_method_names = ['get', 'post']
    
    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)    
    

class GameHistoryViewsets(viewsets.ModelViewSet):
    queryset = GameHistory.objects.all()
    serializer_class = GameHistorySerializer
    http_method_names = ['get', 'post']

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_data(request):
    serializer = ListUserDataSerializer(request.user)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
