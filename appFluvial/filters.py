from django import forms
import django_filters
from .models import Viaje, Destinatario, Carga, Pago
NOMBRE_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('Pasaporte', 'Pasaporte'),
    ]

class ViajeFilter(django_filters.FilterSet):
    fecha_inicio_viaje = django_filters.DateFilter(
        field_name='Fecha_inicio_viaje',
        lookup_expr='exact',  
        label='Fecha de Inicio del Viaje',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Viaje
        fields = {
            'Guía_zarpe': ['exact'],
            # Agrega más campos según sea necesario Fecha_inicio_viaje
        }

class DestinatarioFilter(django_filters.FilterSet):
    """
    tipodocumento = django_filters.ModelChoiceFilter(
        field_name='tipodocumento',
        label='Tipo de Documento',
        choices=[('CC', 'Cédula de Ciudadanía'),('CE', 'Cédula de Extranjería'),('Pasaporte', 'Pasaporte'),],
        empty_label='Seleccionar',
        lookup_expr='exact'
    )"""
    #fname = django_filters.CharFilter(lookup_expr='icontains', label='Nombre')

    class Meta:
        model = Destinatario
        fields = {
            'fname': ['exact', 'icontains'],
            # Agrega más campos según sea necesario
        }
    

class CargaFilter(django_filters.FilterSet):
    class Meta:
        model = Carga
        fields = {
            'tipo_carga': ['exact', 'icontains'],
            'unidad_medida': ['exact', 'icontains'],
            'categoria': ['exact', 'icontains'],
            'ruta': ['exact', 'icontains'],
            'asegurar_carga': ['exact', 'icontains'],
            # Agrega más campos según sea necesario
        }

class PagoFilter(django_filters.FilterSet):
    class Meta:
        model = Pago
        fields = {
            'fecha_transaccion': ['exact', 'icontains'],
            'tipo_pago': ['exact', 'icontains'],
            # Agrega más campos según sea necesario
        }
