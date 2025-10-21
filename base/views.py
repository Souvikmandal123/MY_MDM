from django.shortcuts import render

# Create your views here.
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

from base.models import Device, Command
from base.tasks import send_command_task

@api_view(["POST"])
def create_command(request):
    """
    POST /api/create_command/
    body: {"device_id": "device001", "command": "ls -la"}
    """
    device_id = request.data.get("device_id")
    command_text = request.data.get("command")
    if not device_id or not command_text:
        return Response({"error": "device_id and command required"}, status=400)

    try:
        device = Device.objects.get(device_id=device_id)
    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=404)

    command_id = str(uuid.uuid4())
    cmd = Command.objects.create(
        command_id=command_id,
        device=device,
        command=command_text,
        status="queued",
        created_at=timezone.now()
    )

    # enqueue Celery task to publish to MQTT
    send_command_task.delay(device_id, command_id, command_text)

    return Response({
        "status": "queued",
        "command_id": command_id,
        "device_id": device_id
    })


@api_view(['GET'])
def list_devices(request):
    devices = Device.objects.all().values('device_id', 'name', 'last_seen')
    return Response(list(devices))

@api_view(['POST'])
def add_device(request):
    device_id = request.data.get('device_id')
    name = request.data.get('name', '')
    if not device_id:
        return Response({'error': 'device_id required'}, status=400)
    device, created = Device.objects.get_or_create(device_id=device_id, defaults={'name': name})
    if not created:
        return Response({'error': 'Device already exists'}, status=400)
    return Response({'status': 'ok', 'device_id': device.device_id, 'name': device.name})

def dashboard(request):
    return render(request, "templates/base/index.html")