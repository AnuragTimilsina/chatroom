# Consumer in web socket is more like a regular django view.

from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class ChatRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        # Extracting room_name from socket url:
        self.room_name = self.scope['url_route']['kwargs']['room_name'] 
        self.room_group_name = 'chat_%s' % self.room_name
        
        # adding the groups using the channels: 
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # After the group is created,
        # We might want to send confirmation!
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tester_message',
                'tester': 'Hi all!',
            }
        )

    async def tester_message(self, event):
        tester = event['tester']

        await self.send(text_data=json.dumps({
            'tester': tester,
        }))
    

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )