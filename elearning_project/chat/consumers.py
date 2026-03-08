from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # setup room group and accept connection
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # handle incoming message
        data = json.loads(text_data)
        message = data["message"]

        # get user name (authenticated or anonymous)
        user_obj = self.scope["user"]
        if user_obj.is_authenticated:
            try:
                profile = await database_sync_to_async(lambda: user_obj.userprofile)()
                user = profile.real_name or user_obj.username
            except Exception:
                user = user_obj.username
        else:
            user = "Anonymous"

        # broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "user": user}
        )

    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "user": event["user"],
        }))
