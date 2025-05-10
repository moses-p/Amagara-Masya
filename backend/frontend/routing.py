from django.urls import re_path
from .consumers import AnomalyConsumer

websocket_urlpatterns = [
    re_path(r'ws/anomalies/$', AnomalyConsumer.as_asgi()),
] 