from django.db import models
from django.contrib.auth import get_user_model

class Queue(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='queues')

class Bot(models.Model):
    name = models.CharField(max_length=50)
    difficulty_level = models.IntegerField(default=1)
    image = models.ImageField(upload_to='bot_images/', blank=True, null=True) 

    def __str__(self):
        return f"{self.name} (Level {self.difficulty_level})"

class GameSession(models.Model):
    first_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='first_user_game_sessions', blank=True, null=True)
    second_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='second_user_game_sessions', blank=True, null=True)
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=models.CASCADE, related_name='games_with_bot')
    winner = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='games_won')
    game_started = models.DateTimeField(auto_now_add=True)
    game_ended = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Game Session between {self.first_user} and {self.second_user or self.bot} started on {self.game_started}"

    def set_winner(self, winner):
        self.winner = winner
        self.game_ended = models.DateTimeField.now()
        self.save()

class GameHistory(models.Model):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='game_histories')
    is_bot = models.BooleanField(default=False)
    pits = models.JSONField(default=list)  
    kazan = models.JSONField(default=list) 
    tuzdyq = models.JSONField(default=list)

    def __str__(self):
        return f"Game History for Session {self.game_session.id}"