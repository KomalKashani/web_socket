from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
import django

django.setup()

from app.models import Chat,Group

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print("Websocket Connect...",event)
        print("Channel Layer..",self.channel_layer)
        print('Channel Name...',self.channel_name)

        # to get the group name from url of web socket
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        print("Group Name:",self.group_name)

        # add channels to new or existing group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self,event):
        print("Message from client...",event['text'])
        print("Type of Message from client...",type(event['text']))
        data = json.loads(event['text'])
        group = Group.objects.get(name= self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(group = group,content = data['msg'])
            chat.save()
            data['user'] = self.scope['user'].username
            print("Data:",data)
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type':'chat.message',
                    'message':json.dumps(data)
                })
        else:
            self.send({
            'type':'websocket.send',
            'text':json.dumps({"msg":"Login ","user":"guest"})
            })

        
    def chat_message(self,event):
        print("Message:",event['message'])
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    def websocket_disconnect(self,event):
        print("Websocket disconnect...",event)
        print("Channel Layer",self.channel_layer)
        print("Channel Name...",self.channel_name)

        # At connection time we create the group and at disconnect we need to discard the group and channels
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()


# All the functions and methods of channel layers are asynchronous and if we use that functions in Synchronous Consumers we need to make that functions from async to sync 
#  and for that we use 

# NOTE = Run this by command /home/komalk/django_rest_framework_project/django-env/bin/python -m daphne -b 0.0.0.0 -p 8000 django_channels.asgi:application

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("Websocket Connect...",event)
        print("Channel Layer..",self.channel_layer)
        print('Channel Name...',self.channel_name)

        # to get the group name from url of web socket
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        print("Group Name:",self.group_name)

        # add channels to new or existing group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self,event):
        print("Message from client...",event['text'])
        print("Type of Message from client...",type(event['text']))
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'chat.message',
                'message':event['text']
            })
        
    async def chat_message(self,event):
        print(event['message'])
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    async def websocket_disconnect(self,event):
        print("Websocket disconnect...",event)
        print("Channel Layer",self.channel_layer)
        print("Channel Name...",self.channel_name)

        # At connection time we create the group and at disconnect we need to discard the group and channels
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()
