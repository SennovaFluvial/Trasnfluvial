# Generated by Django 3.2.23 on 2023-12-01 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFluvial', '0013_alter_carga_asegurar_carga'),
    ]

    operations = [
        migrations.AddField(
            model_name='carga',
            name='factorSeguro',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carga',
            name='total',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]