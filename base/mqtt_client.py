import paho.mqtt.client as mqtt
import os
import json
from base.models import *

# Read broker info from environment

MQTT_BROKER = "d0365b492a9a43e9b554a8c64db33572.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "hivemq.webclient.1761500101022"
MQTT_PASSWORD = "cgR0d18Vf!3#zy*UDT&S"
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
