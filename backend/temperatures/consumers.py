# -*- coding: utf-8 -*-
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
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
