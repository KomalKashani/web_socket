from api.consumers import MySyncConsumer,MyAsyncConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/sc/',MySyncConsumer.as_asgi()),
    path('ws/ac/',MyAsyncConsumer.as_asgi())

]