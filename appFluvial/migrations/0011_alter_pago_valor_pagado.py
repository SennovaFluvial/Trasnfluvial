# Generated by Django 3.2.23 on 2023-11-30 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFluvial', '0010_auto_20231130_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='valor_pagado',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
    ]
