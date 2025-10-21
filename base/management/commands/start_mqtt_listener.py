from django.core.management.base import BaseCommand
from base.mqtt_listener import start

class Command(BaseCommand):
    help = "Start MQTT listener to receive device results"

    def handle(self, *args, **options):
        self.stdout.write("Starting MQTT listener...")
        start()
