import uuid
import datetime
import re

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.generics import ListAPIView
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from temperatures import serializers
from temperatures import models

DUMMY_UUID = uuid.UUID('12345678123456781234567812345678')
DELAY = 60


@require_http_methods(["GET"])
def index(request):
    return render(request,
                  context={"device_uuid": str(DUMMY_UUID)},
                  template_name="index.html")


class Temperatures(ListAPIView):
    serializer_class = serializers.TemperatureSerializer

    def get_queryset(self):
        since = self.request.query_params.get("since", None)

        if since:
            return models.Temperature.objects.filter(datetime__gte=since)
        return models.Temperature.objects.all()


def launch_temp_parsing(temperature: models.Temperature):
    print(f"Parsing temp {temperature.temperature}")
    async_to_sync(get_channel_layer().send)(
        "parse-temperature",
        {
            "type": "parse_temperature",
            "temperature": serializers.TemperatureSerializer().to_representation(temperature)
        }
    )


@require_http_methods(["POST"])
@csrf_exempt
def receive_temperatures(request):
    device, _ = models.Device.objects.get_or_create(identifier=DUMMY_UUID)
    channel_layer = get_channel_layer()

    data = bytearray(request.POST.get("data"), encoding='utf-8')
    temperatures = list()
    for i in range(0, len(data), 2):
        temperatures.append(int(data[i:i+2], 16))

    timestamp = timezone.now()

    for temperature in temperatures:
        print(f"adding temperature {temperature}")
        temp = models.Temperature.objects.create(
            temperature=temperature,
            device=device,
            datetime=timestamp)

        timestamp = timestamp - datetime.timedelta(seconds=DELAY)

        async_to_sync(channel_layer.group_send)(
            str(device.identifier),
            {
                "type": "temperature",
                "temperature": serializers.TemperatureSerializer().to_representation(temp)
            }
        )
        launch_temp_parsing(temp)

    return HttpResponse()
