from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import path
from django.contrib.auth.models import AnonymousUser
import json

from chat.models import Message
from chat.consumers import ChatConsumer
from users.models import UserProfile

User = get_user_model()

class MessageModelTest(TestCase):
    def setUp(self):
        # create user + profile + sample message
        self.user = User.objects.create(username="sam")
        self.profile = UserProfile.objects.create(user=self.user, real_name="Sam")
        self.message = Message.objects.create(sender=self.profile, content="Hello!")

    def test_message_str(self):
        # check __str__ output and sender link
        self.assertIn("Hello", str(self.message))
        self.assertEqual(self.message.sender, self.profile)


class ChatRoomViewTest(TestCase):
    def setUp(self):
        # client + sample message
        self.client = Client()
        self.user = User.objects.create(username="sam")
        self.profile = UserProfile.objects.create(user=self.user, real_name="Sam")
        Message.objects.create(sender=self.profile, content="Hi there")

    def test_chat_room_renders(self):
        # ensure chat section appears in dashboard
        response = self.client.get("/chat_room/")  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chat Room")  


class ChatConsumerTest(TestCase):
    async def test_websocket_chat(self):
        # setup communicator for test room
        application = URLRouter([
            path("ws/chat/<room_name>/", ChatConsumer.as_asgi()),
        ])

        communicator = WebsocketCommunicator(application, "/ws/chat/testroom/")
        communicator.scope["user"] = AnonymousUser()  # inject test user

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # send and receive test message
        await communicator.send_json_to({"message": "Hello world"})
        response = await communicator.receive_json_from()

        self.assertEqual(response["message"], "Hello world")
        self.assertIn("user", response)

        await communicator.disconnect()
