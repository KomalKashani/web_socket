from django.urls import path
from api.consumers import MySyncConsumer,MyAsyncConsumer

websocket_urlpatterns = [
    path('ws/sc/',MySyncConsumer.as_asgi()),
    path('ws/ac/',MyAsyncConsumer.as_asgi())

]