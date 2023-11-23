from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import GameSessionViewsets, GameHistoryViewsets

router = DefaultRouter()
router.register(r'game_sessions', GameSessionViewsets)
router.register(r'game_histories', GameHistoryViewsets)

urlpatterns = [
    path('', include(router.urls)),
]