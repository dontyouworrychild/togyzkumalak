from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import GameSessionViewsets, GameHistoryViewsets
from . import consumers

router = DefaultRouter()
router.register(r'game_sessions', GameSessionViewsets)
router.register(r'game_histories', GameHistoryViewsets)

from .views import user_game_stats

websocket_urlpatterns = [
    path('ws/games/<int:game_session_id>/', consumers.GameConsumer.as_asgi()),
]

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', user_game_stats, name='user-stats'),
]