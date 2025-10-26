import uuid
from celery import shared_task
from .mqtt_client import publish_command
from .models import Command

@shared_task(bind=True)
def send_command_task(self, device_id: str, command_id: str, command_text: str):
    """
    Celery task that publishes command to MQTT and updates DB status to 'sent'.
    """
    try:
        publish_command(device_id, command_id, command_text)
        Command.objects.filter(command_id=command_id).update(status="sent")
        return {"status": "ok", "command_id": command_id}
    except Exception as e:
        # Optionally retry on failure
        raise self.retry(exc=e, countdown=5, max_retries=3)
