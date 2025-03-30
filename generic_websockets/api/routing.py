from django.urls import path
from api.consumers import MyWebsocketConsumer,MyAsyncWebsocketConsumer

websocket_urlpatterns = [
    path('ws/wsc/<str:groupkaname>/',MyWebsocketConsumer.as_asgi()),
    path('ws/awsc/<str:groupkaname>/',MyAsyncWebsocketConsumer.as_asgi())
]