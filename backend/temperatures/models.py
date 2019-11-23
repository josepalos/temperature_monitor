from django.db import models


class Device(models.Model):
    identifier = models.UUIDField()


class Temperature(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    temperature = models.IntegerField()

    class Meta:
        get_latest_by = "order_date"
