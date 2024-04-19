# """
# ASGI config for senior project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# """
# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import togyzkumalak.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senior.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             togyzkumalak.routing.websocket_urlpatterns
#         )
#     ),
# })

import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the 'asgi' process.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senior.settings')

# Get the ASGI application before importing channels layers
django_asgi_app = get_asgi_application()

# Import after setting the environment variable and getting the ASGI application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from togyzkumalak.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Django's ASGI application for handling HTTP requests
    "websocket": AuthMiddlewareStack(  # WebSocket handler with Django authentication
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
