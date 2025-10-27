from django.urls import path
from base.views import *
from . import views

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("api/create_command/", create_command, name="create_command"),
    path("api/devices/", list_devices, name="list_devices"),
    path("api/devices/add/", add_device, name="add_device"),
    path('api/devices/delete/<int:device_id>/', views.delete_device, name='delete_device'),
    path('api/command_status/', views.update_command_status, name='update_command_status'),
    path('device/<int:device_id>/', views.device_detail_page, name='device_detail_page'),
    path('api/device/<int:device_id>/', views.device_detail_api, name='device_detail_api'),
]