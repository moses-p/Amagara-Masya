import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from core.consumers import DashboardConsumer
from frontend.routing import websocket_urlpatterns as frontend_ws_patterns
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amagara_masya.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/dashboard/", DashboardConsumer.as_asgi()),
            *frontend_ws_patterns,
        ])
    ),
}) 