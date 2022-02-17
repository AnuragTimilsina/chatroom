from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import public_chat.routing

application = ProtocolTypeRouter({
        # Wrapping websocket with authentication.  
       'websocket': AuthMiddlewareStack(
           URLRouter(
               public_chat.routing.websocket_urlpatterns
           )
       ),
})