from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from time import sleep
from asgiref.sync import async_to_sync
import asyncio
import json
import os
import django
from channels.db import database_sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'generic_websockets.settings')  # Replace with your project name
django.setup()
from api.models import Chat,Group


class MyWebsocketConsumer(WebsocketConsumer):
    def connect(self):
        print("Websocket Connect")
        print("Channel layer...",self.channel_layer)
        print("Channel Name: ", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print("Group Name: ",self.group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def receive(self,text_data = None, bytes_data = None):
        print("Message Received from client...",text_data)
        data = json.loads(text_data)
        data['msg'] = data['msg']
        group = Group.objects.get(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content = data['msg'],
                group = group
            )
            data['user'] = self.scope['user'].username
            chat.save()
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type':'chat.message',
                    'message': json.dumps(data)
                }
            )
        else:
            self.send(text_data = json.dumps({
                'msg':'Login Required','user':'guest'
            }))


    def chat_message(self,event):
        print("Chat message:",event)
        print(event['message'])
        self.send(text_data=event['message'])

    def disconnect(self, close_code):
        print("Websocket Disconnected...",close_code)
        async_to_sync(self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        ))

class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Websocket Connect")
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print("Group Name: ",self.group_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self,text_data = None, bytes_data = None):
        print("Message Received from client...",text_data)
        data = json.loads(text_data)
        message = data['msg']
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        chat = Chat(
            content = data['msg'],
            group = group
        )
        await database_sync_to_async(chat.save)()
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'chat.message',
                'message': message
            }
        )
    async def chat_message(self,event):
        print("Chat message:",event)
        print(event['message'])
        await self.send(text_data=json.dumps({'msg':event['message']}))


    async def disconnect(self, close_code):
        print("Websocket Disconnected...",close_code)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
