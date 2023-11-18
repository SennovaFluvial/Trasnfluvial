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
        guainia, _ = Departamento.objects.get_or_create(nombre='Guainía')
        vaupes, _ = Departamento.objects.get_or_create(nombre='Vaupés')

        
        Municipio.objects.get_or_create(nombre='Calamar', departamento=guaviare)
        Municipio.objects.get_or_create(nombre='El Retorno', departamento=guaviare)
        Municipio.objects.get_or_create(nombre='Miraflores', departamento=guaviare)
        Municipio.objects.get_or_create(nombre='Barranquillita', departamento=guaviare)
        Municipio.objects.get_or_create(nombre='San José del Guaviare', departamento=guaviare)

        
        Municipio.objects.get_or_create(nombre='Cumaribo', departamento=vichada)
        Municipio.objects.get_or_create(nombre='La Primavera', departamento=vichada)     
        Municipio.objects.get_or_create(nombre='Puerto Carreño', departamento=vichada)
        Municipio.objects.get_or_create(nombre='Santa Rosalía', departamento=vichada)
        Municipio.objects.get_or_create(nombre='Santa Rita', departamento=vichada)
        
        Municipio.objects.get_or_create(nombre='Mapiripan', departamento=meta)

        Municipio.objects.get_or_create(nombre='Inirida', departamento=guainia)
        Municipio.objects.get_or_create(nombre='Barrancominas', departamento=guainia)
        Municipio.objects.get_or_create(nombre='Raudal de la mapiripana', departamento=guainia)

        Municipio.objects.get_or_create(nombre='Carurú', departamento=vaupes)
        Municipio.objects.get_or_create(nombre='Pucarón', departamento=vaupes)
        Municipio.objects.get_or_create(nombre='Mitú', departamento=vaupes)

        self.stdout.write(self.style.SUCCESS('Data populated successfully!'))
