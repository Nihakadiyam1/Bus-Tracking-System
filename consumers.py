import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BusLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.bus_number = self.scope['url_route']['kwargs']['bus_number']
        self.group_name = f'bus_{self.bus_number}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_location(self, event):
        await self.send(text_data=json.dumps(event['data']))
