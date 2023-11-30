# tables.py
import django_tables2 as tables
from .models import Viaje

class TuModeloTable(tables.Table):
    class Meta:
        model = Viaje
        template_name = 'django_tables2/bootstrap4.html'  # Puedes cambiar la plantilla según tus necesidades
