from django.urls import path
from notification.consumer import NotificationConsumer

websocket_urlpatterns = [
    path('notifications', NotificationConsumer.as_asgi()),
]
