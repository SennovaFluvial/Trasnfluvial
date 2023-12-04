# Generated by Django 3.2.23 on 2023-12-03 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFluvial', '0017_auto_20231201_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pago',
            name='pagoefectivo',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='pagotransferencia',
        ),
        migrations.AddField(
            model_name='pago',
            name='tipo_pago',
            field=models.CharField(blank=True, choices=[('pago en efectivo', 'pago en efectivo'), ('pago por transferencia', 'pago por transferencia')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pago',
            name='valor_pagado',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True),
        ),
    ]