# -*- coding: utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    path("new_temperature", views.receive_temperatures)
]