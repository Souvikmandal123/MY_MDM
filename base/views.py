from django.shortcuts import render

# Create your views here.
import uuid
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

from base.models import Device, Command
from base.tasks import send_command_task
from django.http import JsonResponse
from .models import Device
from django.views.decorators.csrf import csrf_exempt
from base.mqtt_client import publish_command 

@csrf_exempt
def create_command(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)
    device_id = data.get("device_id")
    command_text = data.get("command")

    command_id = str(uuid.uuid4())
    device = Device.objects.get(device_id = device_id)

    Command.objects.create(
        command_id = command_id,
        device = device,
        command = command_text,
        status = "queued",
        created_at = timezone.now()
    )

    # Publish to MQTT
    publish_command(device_id, command_id, command_text)

    return JsonResponse({"command_id": command_id})


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
    return render(request, "base/index.html")

@csrf_exempt
def delete_device(request, device_id):
    if request.method == "DELETE":
        try:
            device = Device.objects.get(device_id=device_id)
            device.delete()
            return JsonResponse({"status": "success", "message": "Device deleted"})
        except Device.DoesNotExist:
            return JsonResponse({"error": "Device not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def update_command_status(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        device_id = data.get("device_id")
        command_id = data.get("command_id")
        status = data.get("status")
        output = data.get("output", "")

        if not all([device_id, command_id, status]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        # device = Device.objects.get(device_id=device_id)
        command = Command.objects.get(command_id=command_id)

        command.status = status
        command.result = output
        command.result_received_at = timezone.now()
        command.save()

        return JsonResponse({"message": "Status updated successfully"})

    except Device.DoesNotExist:
        return JsonResponse({"error": "Device not found"}, status=404)
    except Command.DoesNotExist:
        return JsonResponse({"error": "Command not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)