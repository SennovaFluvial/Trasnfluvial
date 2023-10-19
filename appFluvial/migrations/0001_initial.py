# Generated by Django 3.2.20 on 2023-08-15 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carga',
            fields=[
                ('ID_Carga', models.AutoField(primary_key=True, serialize=False)),
                ('Descripción', models.TextField()),
                ('Peso', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Origen', models.CharField(max_length=100)),
                ('Destino', models.CharField(max_length=100)),
                ('Tipo_carga', models.CharField(max_length=100)),
                ('Estado_carga', models.CharField(max_length=100)),
                ('Fecha_transporte', models.DateField()),
                ('Otros_detalles', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('ID_Cargo', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre_cargo', models.CharField(max_length=100)),
                ('Descripción_cargo', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('ID_Cliente', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=100)),
                ('Dirección', models.CharField(max_length=200)),
                ('Teléfono_contacto', models.CharField(max_length=15)),
                ('Otros_contacto', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Destinatario',
            fields=[
                ('ID_Destinatario', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=100)),
                ('Dirección', models.CharField(max_length=200)),
                ('Teléfono_contacto', models.CharField(max_length=15)),
                ('Otros_contacto', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaTransporteFluvial',
            fields=[
                ('ID_Empresa', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=100)),
                ('Dirección', models.CharField(max_length=200)),
                ('Teléfono', models.CharField(max_length=15)),
                ('Tipo_empresa', models.CharField(choices=[('PN', 'Persona Natural o Núcleo Familiar'), ('PJ', 'Persona Jurídica')], max_length=2)),
                ('NIT', models.CharField(max_length=20)),
                ('Fecha_fundación', models.DateField()),
                ('Número_empleados', models.PositiveIntegerField()),
                ('Área_operación', models.CharField(max_length=100)),
                ('Ruta_principal', models.CharField(max_length=100)),
                ('Sitio_web', models.URLField(blank=True, null=True)),
                ('Correo_contacto', models.EmailField(blank=True, max_length=254, null=True)),
                ('Número_embarcaciones', models.PositiveIntegerField()),
                ('Capacidad_total_carga', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Número_viajes_mes', models.PositiveIntegerField()),
                ('Servicios_adicionales', models.TextField(blank=True, null=True)),
                ('Estado_registro', models.CharField(max_length=50)),
                ('Licencias_permisos_vigentes', models.TextField(blank=True, null=True)),
                ('Nivel_tecnificación_actual', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Motonave',
            fields=[
                ('ID_Motonave', models.AutoField(primary_key=True, serialize=False)),
                ('Número_patente', models.CharField(max_length=50)),
                ('Capacidad_carga', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Estado', models.CharField(choices=[('Activa', 'Activa'), ('Inactiva', 'Inactiva'), ('Reparación', 'En Reparación')], max_length=20)),
                ('Otros_atributos', models.TextField(blank=True, null=True)),
                ('Tipo_comunicación', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('ID_Parameter', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('ID_Persona', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=50)),
                ('Apellido', models.CharField(max_length=50)),
                ('Correo', models.EmailField(max_length=254)),
                ('Teléfono', models.CharField(max_length=15)),
                ('Cédula_identidad', models.CharField(max_length=20)),
                ('Seguro_social', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Viaje',
            fields=[
                ('ID_Viaje', models.AutoField(primary_key=True, serialize=False)),
                ('Guía_zarpe', models.CharField(max_length=100)),
                ('Fecha_inicio_viaje', models.DateField()),
                ('Fecha_fin_viaje', models.DateField(blank=True, null=True)),
                ('Carga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFluvial.carga')),
                ('Motonave', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFluvial.motonave')),
                ('Piloto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFluvial.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Negocio',
            fields=[
                ('ID_Negocio', models.AutoField(primary_key=True, serialize=False)),
                ('Fecha_inicio', models.DateField()),
                ('Fecha_fin', models.DateField(blank=True, null=True)),
                ('Cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFluvial.cliente')),
                ('Destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFluvial.destinatario')),
                ('Empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFluvial.empresatransportefluvial')),
            ],
        ),
    ]