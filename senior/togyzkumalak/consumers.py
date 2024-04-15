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
