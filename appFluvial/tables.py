# tables.py
import django_tables2 as tables
from .models import Carga, Destinatario, Pago, Viaje

class TuModeloTableViaje(tables.Table):
    class Meta:
        model = Viaje
        template_name = 'django_tables2/bootstrap4.html'  # Puedes cambiar la plantilla según tus necesidades

class TuModeloTableCarga(tables.Table):
    class Meta:
        model = Carga
        template_name = 'django_tables2/bootstrap4.html'  # Puedes cambiar la plantilla según tus necesidades

class TuModeloTablePago(tables.Table):
    class Meta:
        model = Pago
        template_name = 'django_tables2/bootstrap4.html'  # Puedes cambiar la plantilla según tus necesidades

class TuModeloTableDestinatario(tables.Table):
    class Meta:
        model = Destinatario
        template_name = 'django_tables2/bootstrap4.html'  # Puedes cambiar la plantilla según tus necesidades

