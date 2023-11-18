# populate_data.py

from django.core.management.base import BaseCommand
from appFluvial.models import Departamento, Municipio

class Command(BaseCommand):
    help = 'Populate data for San José del Guaviare, Vichada, and Meta'

    def handle(self, *args, **options):
        # Crear departamentos
        guaviare, _ = Departamento.objects.get_or_create(nombre='Guaviare')
        vichada, _ = Departamento.objects.get_or_create(nombre='Vichada')
        meta, _ = Departamento.objects.get_or_create(nombre='Meta')

        
        Municipio.objects.get_or_create(nombre='Calamar', departamento=guaviare)
        Municipio.objects.get_or_create(nombre='El Retorno', departamento=guaviare)
        Municipio.objects.get_or_create(nombre='Miraflores', departamento=guaviare)
        Municipio.objects.get_or_create(nombre='San José del Guaviare', departamento=guaviare)

        
        Municipio.objects.get_or_create(nombre='Cumaribo', departamento=vichada)
        Municipio.objects.get_or_create(nombre='La Primavera', departamento=vichada)
        Municipio.objects.get_or_create(nombre='San José de Ocune', departamento=vichada)        
        Municipio.objects.get_or_create(nombre='Puerto Carreño', departamento=vichada)
        Municipio.objects.get_or_create(nombre='Santa Rosalía', departamento=vichada)
        Municipio.objects.get_or_create(nombre='Santa Rita', departamento=vichada)
        
        Municipio.objects.get_or_create(nombre='Caño jabón', departamento=meta)

        self.stdout.write(self.style.SUCCESS('Data populated successfully!'))
