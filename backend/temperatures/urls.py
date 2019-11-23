# -*- coding: utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("temperatures", views.Temperatures.as_view()),
    path("new_temperature", views.receive_temperatures),
]
