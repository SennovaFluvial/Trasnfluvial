# Generated by Django 3.1.2 on 2020-10-17 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201016_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=70)),
                ('Ruta', models.CharField(max_length=70)),
                ('Desccripcion', models.CharField(max_length=70)),
                ('Imagen', models.CharField(max_length=70)),
                ('idRoll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.roll')),
            ],
            options={
                'db_table': 'menu',
            },
        ),
    ]
