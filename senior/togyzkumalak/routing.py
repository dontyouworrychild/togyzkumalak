
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import path
# from . import consumers

# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             path("ws/game/<int:game_session_id>/", consumers.GameConsumer.as_asgi()),
#         ])
#     ),
# })


from django.urls import re_path
from .consumers import QueueConsumer

websocket_urlpatterns = [
    re_path(r'ws/matchmaking/$', QueueConsumer.as_asgi()),
]