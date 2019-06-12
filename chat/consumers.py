import datetime

import pudb
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.utils import timezone

from chat.models import Chat, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = (f'{self.scope["user"].first_name} '
                   f'{self.scope["user"].first_name} '
                   f'{timezone.now().strftime("%Y.%m.%d %H:%M:%S")} '
                   f'{text_data_json["message"]}')
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        # add message to db
        chat = Chat.objects.get(
            theme=self.scope['url_route']['kwargs']['room_name'])
        ChatMessage.objects.create(message=message, chat=chat)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
