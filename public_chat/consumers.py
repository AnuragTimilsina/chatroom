# Consumer in web socket is more like a regular django view.

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extracting room_name from socket url:
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        #     #     # Trying out tester message:
    #     #     await self.channel_layer.group_send(
    #     #         self.room_group_name,
    #     #         {
    #     #             'type': 'tester_message',
    #     #             'tester': 'Hi all!',
    #     #         }
    #     #     )

    #     # async def tester_message(self, event):
    #     #     tester = event['tester']

    #     #     await self.send(text_data=json.dumps({
    #     #         'tester': tester,
    #     #     }))
    

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # handling chat input from the frontend:
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))