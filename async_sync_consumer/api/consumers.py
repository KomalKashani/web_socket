from channels.consumer import SyncConsumer,AsyncConsumer,StopConsumer

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print("Websocket Connect...",event)
        self.send({
            'type': 'websocket.accept',
        })

    def websocket_receive(self,event):
        print("Websocket Receive...",event)
        print(event['text'])
        self.send({
            'type':'websocket.send',
            'text': 'Message sent to client'
        })
    def websocket_disconnect(self,event):
        print("Websocket Disconnect")
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("Websocket Connect...",event)
        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self,event):
        print("Websocket Receive...",event)
        print(event['text'])
        await self.send({
            'type':'websocket.send',
            'text': 'Message sent to client'
        })
    async def websocket_disconnect(self,event):
        print("Websocket Disconnect")
        raise StopConsumer()