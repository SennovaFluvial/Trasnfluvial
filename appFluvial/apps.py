from django.apps import AppConfig
from django.core.management import call_command

class AppfluvialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appFluvial'
    
    def ready(self):
        call_command('loaddata', 'initial_data.json')