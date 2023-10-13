# Generated by Django 3.1.2 on 2020-10-19 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_auto_20201016_2301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dependencia',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=70)),
            ],
            options={
                'db_table': 'dependencia',
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=70)),
                ('apellidos', models.CharField(max_length=70)),
                ('correo', models.CharField(max_length=70)),
                ('cedula', models.CharField(max_length=70)),
                ('dependencia', models.CharField(max_length=70)),
                ('jefeInmeddiato', models.CharField(max_length=70)),
                ('diligencia', models.CharField(max_length=100)),
                ('justifiacion', models.CharField(max_length=300)),
                ('token', models.CharField(max_length=70)),
                ('estado', models.CharField(max_length=70)),
                ('documento', models.CharField(max_length=70)),
                ('idUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleUser',
            fields=[
                ('idUser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('tipoContrato', models.CharField(max_length=70)),
                ('idjefe', models.BigIntegerField()),
                ('telefono', models.CharField(max_length=70)),
                ('direccion', models.CharField(max_length=70)),
                ('cedula', models.CharField(max_length=70)),
                ('idDependencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.dependencia')),
            ],
            options={
                'db_table': 'detalle_usuario',
            },
        ),
    ]
