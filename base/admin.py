from django.contrib import admin
from .models import Device, Command

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("device_id", "name", "last_seen")

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ("command_id", "device", "status", "created_at", "result_received_at")
    readonly_fields = ("created_at", "result_received_at")
