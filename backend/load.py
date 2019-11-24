import random
import uuid
from temperatures import models
import datetime
from django.utils import timezone

first = timezone.now()
offset = datetime.timedelta(minutes=1)
DUMMY_UUID = uuid.UUID('12345678123456781234567812345678')

dades = 3600

device, _ = models.Device.objects.get_or_create(identifier=DUMMY_UUID)

for i in range(0, dades):
    temp = random.randint(0, 40)
    models.Temperature.objects.create(temperature=temp, device=device, datetime=first)
    first = first - offset
