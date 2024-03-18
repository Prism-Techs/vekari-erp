import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from notification.models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = f'user_{self.user.id}'
            print(f"{self.user}({self.user.id}) is connected")
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            notification_count = await self.get_notification_count()
            print(notification_count)
            await self.send(text_data=json.dumps({
                'message': "connected to sockets",
                'notification_count':notification_count
            }))

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def update_notification(self, data):
        await self.send(text_data=json.dumps(data))
    async def send_notification(self, data):
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def get_notification_count(self):
        return Notification.objects.filter(receiver_user=self.user.id, is_read=0).count()
