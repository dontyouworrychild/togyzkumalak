from django.db import models
from django.contrib.auth.models import User

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='game_sessions', null=True)
    # is_user_winner = 

    def __str__(self) -> str:
        return f"Game session for {self.user.first_name} {self.user.last_name}"

class GameHistory(models.Model):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='game_histories')
    pits = models.JSONField(default=list)  
    kazan = models.JSONField(default=list) 
    tuzdyq = models.JSONField(default=list)

    def __str__(self):
        return f"Game History for Session {self.game_session.id}"