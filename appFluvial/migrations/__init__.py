from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appFluvial'

    def ready(self):
        # Importa el modelo aquí para evitar problemas de importación circular
        from models import CardDescription
        # Llama a la función de prellenado de datos
        CardDescription.prepopulate()