# Generated by Django 3.2.23 on 2023-11-25 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFluvial', '0005_auto_20231125_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='carga',
            name='asegurar_carga',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='carga',
            name='cantidad_carga',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='capitan',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='categoria',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='ciudad_carga',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='costo_flete',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='departamento_carga',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='embarcacion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='fecha_cargue',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='fecha_recibo',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='fecha_salida',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='nro_guia',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='peso',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='ruta',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='tipo_carga',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='unidad_medida',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='volumen_carga',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
