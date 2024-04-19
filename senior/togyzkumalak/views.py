from django.shortcuts import render
from django.db.models import Count, Q
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import RegisterSerializer, ListUserDataSerializer, GameSessionSerializer, GameHistorySerializer, QueueSerializer
from django.contrib.auth.models import User
from .models import GameHistory, GameSession, Queue
from .app import ai
from django.db import transaction
from rest_framework.decorators import action


class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_name='match_user')
    def match_user(self, request):
        # Get the user from the request user or payload
        requesting_user = request.user
        
        with transaction.atomic():  # Use a transaction to ensure atomicity
            # Check if there's another user in the queue
            try:
                other_user_queue = Queue.objects.exclude(user=requesting_user).select_for_update().first()
            except Queue.DoesNotExist:
                return Response({'error': 'No other users in queue'}, status=status.HTTP_404_NOT_FOUND)

            if other_user_queue is not None:
                # Create a new GameSession
                game_session = GameSession.objects.create(
                    first_user=requesting_user,
                    second_user=other_user_queue.user
                )

                # Delete the other user's queue entry
                other_user_queue.delete()

                # You may want to delete the requesting user's queue as well
                Queue.objects.filter(user=requesting_user).delete()

                # Return the created game session details
                game_session_serializer = GameSessionSerializer(game_session)
                return Response(game_session_serializer.data, status=status.HTTP_201_CREATED)
            else:
                # If no match was found, optionally add the user to the queue
                Queue.objects.get_or_create(user=requesting_user)
                return Response({'status': 'You are added to the queue and waiting for a match.'}, status=status.HTTP_200_OK)

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