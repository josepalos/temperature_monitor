# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer

from temperatures import models


class TemperatureSerializer(ModelSerializer):
    class Meta:
        model = models.Temperature
        fields = "__all__"
