from django.contrib import admin
from .models import GameHistory, GameSession, Bot

admin.site.register(GameHistory)
admin.site.register(GameSession)
admin.site.register(Bot)