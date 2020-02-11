from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import clotudy_backend.cloredis.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            clotudy_backend.cloredis.routing.websocket_urlpatterns
        )
    ),
})
