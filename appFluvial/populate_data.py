# populate_data.py

from django.core.management.base import BaseCommand
from appFluvial.models import Departamento, Municipio

class Command(BaseCommand):
    help = 'Populate data for San José del Guaviare, Vichada, and Meta'

    def handle(self, *args, **options):
        # Crear departamentos
        san_jose, _ = Departamento.objects.get_or_create(nombre='San José del Guaviare')
        vichada, _ = Departamento.objects.get_or_create(nombre='Vichada')
        meta, _ = Departamento.objects.get_or_create(nombre='Meta')

        # Crear municipios asociados a San José del Guaviare
        Municipio.objects.get_or_create(nombre='Calamar', departamento=san_jose)
        Municipio.objects.get_or_create(nombre='El Retorno', departamento=san_jose)
        Municipio.objects.get_or_create(nombre='Miraflores', departamento=san_jose)
        Municipio.objects.get_or_create(nombre='San José del Guaviare', departamento=san_jose)

        # Crear municipios asociados a Vichada
        Municipio.objects.get_or_create(nombre='Cumaribo', departamento=vichada)
        Municipio.objects.get_or_create(nombre='La Primavera', departamento=vichada)
        Municipio.objects.get_or_create(nombre='San José del Guaviare Ocune', departamento=vichada)

        # Crear municipios asociados a Meta
        Municipio.objects.get_or_create(nombre='Puerto Carreño', departamento=meta)
        Municipio.objects.get_or_create(nombre='Santa Rosalía', departamento=meta)
        Municipio.objects.get_or_create(nombre='Santa Rita', departamento=meta)

        self.stdout.write(self.style.SUCCESS('Data populated successfully!'))
