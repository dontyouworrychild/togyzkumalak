from django.shortcuts import render
from django.db.models import Count, Q
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import RegisterSerializer, ListUserDataSerializer, GameSessionSerializer, GameHistorySerializer
from django.contrib.auth.models import User
from .models import GameHistory, GameSession
from .app import ai


class GameSessionViewsets(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer
    http_method_names = ['get', 'post', 'patch']
    
    def get_permissions(self):
        permission_classes = [AllowAny]
        # if self.action in ['create']:
        #     permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)    
    

class GameHistoryViewsets(viewsets.ModelViewSet):
    queryset = GameHistory.objects.all()
    serializer_class = GameHistorySerializer
    http_method_names = ['get', 'post']

    def create(self, request):
        is_bot = request.data.get('is_bot', False)

        if is_bot:
            response = self.handle_bot_action(request)
        else:
            response = self.handle_human_action(request)
        
        return response
    
    def handle_bot_action(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        pits = request.data.get('pits', [])
        kazan = request.data.get('kazan', [])
        tuzdyq = request.data.get('tuzdyq', [])
        level = request.data.get('level', 1)
        current_player = 1

        state = {}
        state['pits'] = pits
        state['kazan'] = kazan
        state['tuzdyq'] = tuzdyq
        state['current_player'] = current_player
        state['level'] = level


        '''
        "pits": [[9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9]],
        "kazan": [0, 0],
        "tuzdyq": [-1, -1]
        "current_player": 1
        '''
        response = ai(state)
        print(response)

        return Response({'data': response}, status=status.HTTP_201_CREATED)

    def handle_human_action(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_game_stats(request):
    user_id = request.user.id 
    user_stats = {
        'total_games': GameSession.objects.filter(Q(first_user_id=user_id) | Q(second_user_id=user_id) | Q(bot__isnull=False, first_user_id=user_id)).count(),
        'games_won': GameSession.objects.filter(winner_id=user_id).count(),
        'games_lost': GameSession.objects.filter(
            Q(first_user_id=user_id) | Q(second_user_id=user_id),
            ~Q(winner_id=user_id),
            winner__isnull=False
        ).count(),
        'games_vs_bot': GameSession.objects.filter(first_user_id=user_id, bot__isnull=False).count(),
    }

    return Response({'data': user_stats}, status=status.HTTP_200_OK)