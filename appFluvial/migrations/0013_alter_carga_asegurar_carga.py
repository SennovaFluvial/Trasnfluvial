# Generated by Django 3.2.23 on 2023-11-30 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFluvial', '0012_auto_20231130_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carga',
            name='asegurar_carga',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]