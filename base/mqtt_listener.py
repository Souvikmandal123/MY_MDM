"""
MQTT result listener: subscribes to devices/+/results and updates Command objects.

This module provides a start() function that runs the MQTT client loop forever.
Run via the management command: python manage.py start_mqtt_listener
"""
import json
import time
import threading
import paho.mqtt.client as mqtt
from django.conf import settings
from django.utils import timezone

from .models import Command, Device

MQTT_BROKER = getattr(settings, "MQTT_BROKER")
MQTT_PORT = getattr(settings, "MQTT_PORT")
MQTT_USER = getattr(settings, "MQTT_USER")
MQTT_PASS = getattr(settings, "MQTT_PASS")
MQTT_USE_TLS = getattr(settings, "MQTT_USE_TLS")
MQTT_QOS = getattr(settings, "MQTT_QOS", 1)

CLIENT_ID = f"mdm-listener-{int(time.time())}"

def on_connect(client, userdata, flags, rc):
    print("MQTT listener connected with rc:", rc)
    client.subscribe("devices/+/results", qos=MQTT_QOS)
    print("Subscribed to devices/+/results")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        command_id = data.get("command_id")
        device_id = data.get("device_id")
        result_text = data.get("result", "")

        if not command_id or not device_id:
            print("Invalid message, missing fields:", payload)
            return

        try:
            cmd = Command.objects.get(command_id=command_id, device__device_id=device_id)
            cmd.result = result_text
            cmd.status = "completed"
            cmd.result_received_at = timezone.now()
            cmd.save()
            print(f"Updated command {command_id} for device {device_id}")
        except Command.DoesNotExist:
            print(f"Command {command_id} not found for device {device_id}, saving as new record")
            # optionally create placeholder Command or ignore
            try:
                device = Device.objects.get(device_id=device_id)
            except Device.DoesNotExist:
                device = Device.objects.create(device_id=device_id, name="")
            Command.objects.create(
                command_id=command_id,
                device=device,
                command="(unknown)",
                status="completed",
                result=result_text,
                result_received_at=timezone.now()
            )
    except Exception as e:
        print("Error handling MQTT message:", e)

def start():
    client = mqtt.Client(client_id=CLIENT_ID)
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    if MQTT_USE_TLS:
        client.tls_set()  # use system CA certs; for custom CA supply path

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_forever()
