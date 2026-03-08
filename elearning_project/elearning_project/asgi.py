import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter  # route by protocol type
from channels.auth import AuthMiddlewareStack  # attach user info to websocket scope
import chat.routing  # websocket URL patterns for chat app

# set default settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elearning_project.settings")

# ASGI entry point 
# routes HTTP requests to Django, websockets to chat consumers
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
