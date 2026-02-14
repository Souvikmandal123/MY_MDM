import paho.mqtt.client as mqtt
import os
import json
from base.models import *

# Read broker info from environment

MQTT_BROKER = "3fdd414487574679ac24d35b27bad7dd.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "mdm_mqtt"
MQTT_PASSWORD = "Souvik@123"
MQTT_TLS = True


# Create a single MQTT client instance
client = mqtt.Client()

if MQTT_USERNAME:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

if MQTT_TLS:
    client.tls_set()

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()


def publish_command(device_id, command_id, command_text):
    """Publish a command to a specific device topic"""
    topic = f"devices/{device_id}/commands"
    payload = json.dumps({
        "command_id": command_id,
        "command": command_text
    })
    client.publish(topic, payload)
    print(f"Published to {topic}: {payload}")
    cmd_status = Command.objects.get(command_id = command_id)
    cmd_status.status = "sent"
    cmd_status.save()
