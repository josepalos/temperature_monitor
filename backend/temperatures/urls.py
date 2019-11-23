# -*- coding: utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("new_temperature", views.receive_temperatures),
]