from channels.consumer import SyncConsumer,AsyncConsumer,StopConsumer
import asyncio
from time import sleep

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print("Websocket connect...",event)
        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self,event):
        print("Websocket Receive...",event)
        print(event['text'])
        for i in range(0,50):
            self.send({
                'type':'websocket.send',
                'text':str(i)
            })
            sleep(1)

    def websocket_disconnect(self,event):
        print("Websocket Disconnect...",event)
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("Websocket connect...",event)
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self,event):
        print("Websocket Receive...",event)
        print(event['text'])
        for i in range(0,50):
            await self.send({
                'type':'websocket.send',
                'text':str(i)
            })
            await asyncio.sleep(1)

    async def websocket_disconnect(self,event):
        print("Websocket Disconnect...",event)
        raise StopConsumer()


# NOTE= IN SYNC CONSUMER IF WE SEND MULTIPLE REQUEST AT A TIME IT WILL PROCESS ONE THEN OTHER
# BUT IN ASYNC CONSUMER IF WE SEND MULTIPLE REQUEST AT A TIME IT WILL PROCESS IT PARALLELY