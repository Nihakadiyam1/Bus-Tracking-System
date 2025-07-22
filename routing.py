from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/bus/(?P<bus_number>\w+)/$', consumers.BusLocationConsumer.as_asgi()),
]
