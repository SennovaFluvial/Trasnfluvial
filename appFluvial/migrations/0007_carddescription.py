# Generated by Django 3.2.20 on 2023-09-12 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFluvial', '0006_auto_20230901_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardDescription',
            fields=[
                ('id_card', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Nombre Card')),
                ('text', models.CharField(blank=True, max_length=3000, verbose_name='text Card')),
                ('image', models.CharField(blank=True, max_length=500, verbose_name='Nombre Card')),
                ('time', models.CharField(blank=True, max_length=100, verbose_name='Nombre Card')),
            ],
        ),
    ]
