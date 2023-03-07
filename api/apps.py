from django.apps import AppConfig
import os


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    def ready(self):
        if os.environ.get('RUN_MAIN'):
            from . import mqtt
            mqtt.client.loop_start()
            print("Starting loop")

