# -*- coding: utf-8 -*-
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import temperatures.routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        temperatures.routing.websocket_urlpatterns,
    )
})