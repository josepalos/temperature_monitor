# -*- coding: utf-8 -*-
import time

from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from temperatures import serializers, models
from temperatures.views import DUMMY_UUID


class TemperaturesConsumer(JsonWebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            str(DUMMY_UUID),
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            str(DUMMY_UUID),
            self.channel_name
        )

    def receive_json(self, content, **kwargs):
        temperature_data = content["temperature"]
        async_to_sync(self.channel_layer.group_send)(
            str(DUMMY_UUID),
            {
                'type': 'temperature',
                'temperature': temperature_data,
            }
        )

    def temperature(self, event):
        temperature_data = event["temperature"]
        self.send_json({"temperature": temperature_data})


class NotificationsConsumer(JsonWebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            f"notifications-{str(DUMMY_UUID)}",
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            f"notifications-{str(DUMMY_UUID)}",
            self.channel_name
        )

    def receive_json(self, content, **kwargs):
        temperature_data = content["notification"]
        async_to_sync(self.channel_layer.group_send)(
            f"notifications-{str(DUMMY_UUID)}",
            {
                'type': 'notification',
                'notification': temperature_data,
            }
        )

    def notification(self, event):
        notification_data = event["notification"]
        self.send_json({"notification": notification_data})


class TemperatureLogicConsumer(JsonWebsocketConsumer):
    def parse_temperature(self, content):
        time.sleep(4)
        temperature = content["temperature"]["temperature"]
        if temperature > 30:
            message = "temperature is getting fucking hot"
        elif temperature < 10:
            message = "why do I live where the wind hurts my face?"
        else:
            message = "fuck, i can't complain"

        device_identifier = models.Device.objects.get(pk=content["temperature"]["device"]).identifier

        async_to_sync(get_channel_layer().group_send)(
            f"notifications-{str(device_identifier)}",
            {
                "type": "notification",
                "notification": message
            }
        )
