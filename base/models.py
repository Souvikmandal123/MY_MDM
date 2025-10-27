from django.db import models
from django.utils import timezone

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255, blank=True)
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.device_id
    
class DeviceDetails(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name="details")

    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    os_version = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    battery = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    encryption = models.BooleanField(default=True)
    compliance_status = models.CharField(max_length=50, default="Compliant")
    last_sync = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Details for {self.device.name}"

class Command(models.Model):
    command_id = models.CharField(max_length=100, unique=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    command = models.TextField()
    status = models.CharField(max_length=20, default="queued")  # queued, sent, completed
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.TextField(null=True, blank=True)
    result_received_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.command_id} -> {self.device.device_id} ({self.status})"
