from django.urls import path
from base.views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("api/create_command/", create_command, name="create_command"),
    path("api/devices/", list_devices, name="list_devices"),
    path("api/devices/add/", add_device, name="add_device"),
]