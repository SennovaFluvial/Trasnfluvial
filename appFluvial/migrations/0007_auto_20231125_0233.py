# Generated by Django 3.2.23 on 2023-11-25 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appFluvial', '0006_auto_20231125_0227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carga',
            name='Descripción',
        ),
        migrations.RemoveField(
            model_name='carga',
            name='Destino',
        ),
        migrations.RemoveField(
            model_name='carga',
            name='Estado_carga',
        ),
        migrations.RemoveField(
            model_name='carga',
            name='Fecha_transporte',
        ),
        migrations.RemoveField(
            model_name='carga',
            name='Origen',
        ),
        migrations.RemoveField(
            model_name='carga',
            name='Otros_detalles',
        ),
        migrations.RemoveField(
            model_name='carga',
            name='Peso',
        ),
        migrations.RemoveField(
            model_name='carga',
            name='Tipo_carga',
        ),
    ]
