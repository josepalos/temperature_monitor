import uuid

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.generics import ListAPIView

from temperatures import serializers
from temperatures import models

DUMMY_UUID = uuid.UUID('12345678123456781234567812345678')


@require_http_methods(["GET"])
def index(request):
    temperatures = models.Temperature.objects.all()
    return render(request,
                  context={"temperatures": temperatures},
                  template_name="index.html")


class Temperatures(ListAPIView):
    queryset = models.Temperature.objects.all()
    serializer_class = serializers.TemperatureSerializer


@require_http_methods(["POST"])
@csrf_exempt
def receive_temperatures(request):
    device, _ = models.Device.objects.get_or_create(identifier=DUMMY_UUID)

    data = bytearray(request.POST.get("data"), encoding='utf-8')
    temperatures = (int(d) for d in data)
    for temperature in temperatures:
        models.Temperature.objects.create(temperature=temperature,
                                          device=device)

    return HttpResponse()
