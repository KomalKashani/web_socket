
from django.urls import path
from api.views import index

urlpatterns = [
    path('<str:group_name>', index),
]
