from django.db import models


class Device(models.Model):
    identifier = models.UUIDField()


class Temperature(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    temperature = models.IntegerField()
