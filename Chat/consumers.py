import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import WebsocketConsumer
from .models import *
from django.shortcuts import get_object_or_404


class ChatConsumer(WebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.partner_name = self.scope['url_route']['kwargs']['username']
        self.partner = get_object_or_404(User, username=self.partner_name)


        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']

        msg = Message.objects.create(
            sender=self.user,
            receiver=self.partner,
            content=content
        )
