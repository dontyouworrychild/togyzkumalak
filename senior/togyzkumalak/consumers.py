import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import GameSession

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_session_id = self.scope['url_route']['kwargs']['game_session_id']
        self.game_session = await self.get_game_session()
        if not self.game_session:
            await self.close()
        else:
            await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data):
        message = json.loads(text_data)
        # Handle incoming WebSocket messages here
        # For example, update game state and send updates to the opponent
        # You can use self.send() to send messages to the client

    async def get_game_session(self):
        try:
            return await self.get_object_or_404(GameSession, id=self.game_session_id)
        except GameSession.DoesNotExist:
            return None

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import Queue, GameSession  # Replace with your actual app name and models
from .serializers import GameSessionSerializer  # Replace with your actual app name and serializers

class QueueConsumer(AsyncWebsocketConsumer):    
    async def connect(self):
        self.user = self.scope['user']
        
        if self.user.is_authenticated:
            # Accept the WebSocket connection
            await self.accept()
            
            # You might want to add the user to the matchmaking queue here
            await sync_to_async(Queue.objects.get_or_create)(user=self.user)
            
            # Add the user to the group to receive notifications
            await self.channel_layer.group_add("matchmaking", self.channel_name)
        else:
            # Reject the connection if the user is not authenticated
            await self.close()

    async def disconnect(self, close_code):
        # Leave the matchmaking group
        await self.channel_layer.group_discard("matchmaking", self.channel_name)
        
        # You might want to remove the user from the matchmaking queue here
        await sync_to_async(Queue.objects.filter(user=self.user).delete)()

    # Custom handler for match_notification events
    async def match_notification(self, event):
        # Send the match notification to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'match.found',
            'game_session': event['game_session']
        }))
    
    async def receive(self, text_data):
        # You can handle received data from the WebSocket here if needed
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        
        if action == 'join_queue':
            # Add user to the matchmaking queue
            await sync_to_async(Queue.objects.get_or_create)(user=self.user)
            await self.send(text_data=json.dumps({'status': 'You joined the matchmaking queue.'}))
        elif action == 'leave_queue':
            # Remove user from the matchmaking queue
            await sync_to_async(Queue.objects.filter(user=self.user).delete)()
            await self.send(text_data=json.dumps({'status': 'You left the matchmaking queue.'}))