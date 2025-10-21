from django.db import models

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255, blank=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.device_id

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
