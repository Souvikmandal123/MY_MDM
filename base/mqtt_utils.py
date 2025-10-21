import os
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

from django.conf import settings

MQTT_BROKER = getattr(settings, "MQTT_BROKER")
MQTT_PORT = getattr(settings, "MQTT_PORT")
MQTT_USER = getattr(settings, "MQTT_USER")
MQTT_PASS = getattr(settings, "MQTT_PASS")
MQTT_USE_TLS = getattr(settings, "MQTT_USE_TLS")
MQTT_QOS = getattr(settings, "MQTT_QOS", 1)

def publish_command(device_id: str, command_id: str, command_text: str) -> None:
    """
    Publish a JSON command to devices/<device_id>/commands
    """
    topic = f"devices/{device_id}/commands"
    payload = json.dumps({
        "command_id": command_id,
        "device_id": device_id,
        "command": command_text
    })
    auth = {"username": MQTT_USER, "password": MQTT_PASS} if MQTT_USER else None

    # For simple usage, use publish.single (creates a fresh connection each publish)
    publish.single(
        topic,
        payload,
        hostname=MQTT_BROKER,
        port=MQTT_PORT,
        auth=auth,
        qos=MQTT_QOS,
        tls=None if not MQTT_USE_TLS else {}
    )
