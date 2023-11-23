from django.contrib import admin
from .models import GameHistory, GameSession

admin.site.register(GameHistory)
admin.site.register(GameSession)