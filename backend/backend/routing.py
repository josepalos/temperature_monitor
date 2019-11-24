# -*- coding: utf-8 -*-
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter

import temperatures.routing
import temperatures.consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        temperatures.routing.websocket_urlpatterns,
    ),
    "channel": ChannelNameRouter({
        "parse-temperature": temperatures.consumers.TemperatureLogicConsumer,
    })
})