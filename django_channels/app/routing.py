from django.urls import path
from app.consumers import MySyncConsumer,MyAsyncConsumer

websocket_urlpatterns = [
    path('ws/sc/<str:groupname>/',MySyncConsumer.as_asgi()),
    path('ws/ac/<str:groupname>/',MyAsyncConsumer.as_asgi())

]