# -*- coding: utf-8 -*-
from django.urls import re_path

from temperatures import consumers

websocket_urlpatterns = [
    re_path(r'ws/temperatures/$', consumers.TemperaturesConsumer),
]
