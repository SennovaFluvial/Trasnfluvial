import datetime
from django.forms import ValidationError
from django.utils import timezone
import random
import string
import time
from django.db import models
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.db import migrations
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.
# En models.py

from django.db import models

class EmpresaTransporteFluvial(models.Model):
    TIPOS_EMPRESA = (
        ('PN', 'Persona Natural o Núcleo Familiar'),
        ('PJ', 'Persona Jurídica'),
        # Otros tipos de empresa que puedan existir
    )

    ID_Empresa = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    Dirección = models.CharField(max_length=200)
    Teléfono = models.CharField(max_length=15)
    Tipo_empresa = models.CharField(choices=TIPOS_EMPRESA, max_length=2)
    NIT = models.CharField(max_length=20)
    Fecha_fundación = models.DateField()
    Número_empleados = models.PositiveIntegerField()
    Área_operación = models.CharField(max_length=100)
    Ruta_principal = models.CharField(max_length=100)
    Sitio_web = models.URLField(blank=True, null=True)
    Correo_contacto = models.EmailField(blank=True, null=True)
    Número_embarcaciones = models.PositiveIntegerField()
    Capacidad_total_carga = models.DecimalField(max_digits=10, decimal_places=2)
    Número_viajes_mes = models.PositiveIntegerField()
    Servicios_adicionales = models.TextField(blank=True, null=True)
    Estado_registro = models.CharField(max_length=50)
    Licencias_permisos_vigentes = models.TextField(blank=True, null=True)
    Nivel_tecnificación_actual = models.CharField(max_length=10)

    def __str__(self):
        return self.Nombre

class Parameter(models.Model):
    ID_Parameter = models.AutoField(primary_key=True)
    key = models.CharField(max_length=200, blank=True, null=True)
    value = models.CharField(max_length=200, blank=True, null=True)
    max = models.CharField(max_length=200, blank=True, null=True)
    min = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return f"[{self.ID_Parameter}] - key: {self.key} --> value: {self.value}  max : {self.max}   min :{self.min} "
    @classmethod
    def prepopulate(cls):
        print("Prepopulating parameters...")
        parameter =cls(key='factorSeguro1', value='0.03', min='0', max='1000') 
        parameter.save()  
        parameter =cls(key='factorSeguro2', value='0.02', min='1000', max='10000') 
        parameter.save()  
        parameter =cls(key='factorSeguro3', value='0.017', min='10000', max='100000000') 
        parameter.save()  
    @classmethod
    def find_parameter_for_subtotal(cls, subtotal):
        parameters_with_range = cls.objects.exclude(min__isnull=True, max__isnull=True)

        # Buscar el primer parámetro que incluya el subtotal dentro de su rango
        for parameter in parameters_with_range:
            try:
                min_value = float(parameter.min)
                max_value = float(parameter.max)
                subtotal_float = float(subtotal)

                if min_value <= subtotal_float < max_value:
                    return parameter
            except (ValueError, TypeError):
                # Manejar casos en los que los valores no son números válidos
                continue

        return None
   
class Persona(models.Model):
    ID_Persona = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    Apellido = models.CharField(max_length=50)
    Correo = models.EmailField()
    Teléfono = models.CharField(max_length=15)
    Cédula_identidad = models.CharField(max_length=20)
    Seguro_social = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.Nombre} {self.Apellido}"


class Cargo(models.Model):
    ID_Cargo = models.AutoField(primary_key=True)
    Nombre_cargo = models.CharField(max_length=100)
    Descripción_cargo = models.TextField()

    def __str__(self):
        return self.Nombre_cargo

class Departamento(models.Model):
    nombre = models.CharField(max_length=255)

class Municipio(models.Model):
    nombre = models.CharField(max_length=255)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

#admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

#admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento_nombre')  # Agregar la columna del nombre del departamento
    list_filter = ('departamento',)

    def departamento_nombre(self, obj):
        return obj.departamento.nombre

    departamento_nombre.admin_order_field = 'departamento__nombre'
    departamento_nombre.short_description = 'Departamento'
# def load_fixture(apps, schema_editor):
#    from django.core.management import call_command
#    call_command('loaddata', 'initial_data.json')   
    
class Motonave(models.Model):
    ESTADOS_MOTONAVE = (
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
        ('Reparación', 'En Reparación'),
        # Otros estados que puedan existir
    )

    ID_Motonave = models.AutoField(primary_key=True)
    Número_patente = models.CharField(max_length=50)
    nombre_motonave = models.CharField(blank=True, max_length=400)
    Capacidad_carga = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=' Capacidad (Kg)')
    Estado = models.CharField(choices=ESTADOS_MOTONAVE, max_length=20)
    Otros_atributos = models.TextField(blank=True, null=True)
    Tipo_comunicación = models.CharField(max_length=100)
    Canal_Radio = models.CharField(blank=True, max_length=100)
    celular = models.CharField(blank=True, max_length=200)
    
    
    def __str__(self):
        return self.Número_patente
    
class MotonaveAdmin(admin.ModelAdmin):
    list_display = ('ID_Motonave','Número_patente', 'nombre_motonave') 
    list_display_links = ('ID_Motonave','Número_patente', 'nombre_motonave') 
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        
        # Verifica si el campo es 'Peso'
        if db_field.name == 'Capacidad_carga':
            # Agrega '(KG)' a la etiqueta del campo
            field.label = f'{field.label} (KG)'        
        return field


class Carga(models.Model):
    ID_Carga = models.AutoField(primary_key=True) 
    nro_guia = models.CharField(max_length=255, blank=True, null=True)
    ciudad_carga = models.CharField(max_length=255, blank=True, null=True)
    departamento_carga = models.CharField(max_length=255, blank=True, null=True)
    embarcacion = models.CharField(max_length=255, blank=True, null=True)
    capitan = models.CharField(max_length=255, blank=True, null=True)
    tipo_carga = models.CharField(max_length=255, blank=True, null=True)
    cantidad_carga = models.CharField(max_length=255, blank=True, null=True)
    unidad_medida = models.CharField(max_length=255, blank=True, null=True)
    volumen_carga = models.CharField(max_length=255, blank=True, null=True)
    peso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_recibo = models.DateField(blank=True, null=True)
    fecha_cargue = models.DateField(blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    categoria = models.CharField(max_length=255, blank=True, null=True)
    ruta = models.CharField(max_length=255, blank=True, null=True)
    costo_flete = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    asegurar_carga = models.BooleanField(default=False, blank=True, null=True)
    factorSeguro = models.CharField(max_length=255,default='0.15', blank=True, null=True)
    total = models.CharField(max_length=255, blank=True, null=True)
    
   

    def __str__(self):
        #return self.nro_guia
        return f"ID_Carga: {self.ID_Carga},nro_guia: {self.nro_guia},ciudad_carga: {self.ciudad_carga},departamento_carga: {self.departamento_carga},embarcacion: {self.embarcacion},capitan: {self.capitan},tipo_carga: {self.tipo_carga},cantidad_carga: {self.cantidad_carga},unidad_medida: {self.unidad_medida},volumen_carga: {self.volumen_carga},peso: {self.peso},fecha_recibo: {self.fecha_recibo},fecha_cargue: {self.fecha_cargue},fecha_salida: {self.fecha_salida},categoria: {self.categoria},ruta: {self.ruta},costo_flete: {self.costo_flete},descripcion: {self.descripcion},asegurar_carga: {self.asegurar_carga}"

class CargaAdmin(admin.ModelAdmin):
    list_display = ('ID_Carga', 'nro_guia', 'ciudad_carga', 'departamento_carga', 'embarcacion', 'capitan',
                    'tipo_carga', 'cantidad_carga', 'unidad_medida', 'volumen_carga', 'peso', 'fecha_recibo',
                    'fecha_cargue', 'fecha_salida', 'categoria', 'ruta', 'costo_flete', 'descripcion', 'asegurar_carga')
    list_display_links = ('ID_Carga', 'nro_guia')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'peso':
            field.label += ' (KG)'
            
        if db_field.name == 'costo_flete':
            field.label += ' Costo Flete($)'

        return field

class Cliente(models.Model):
    ID_Cliente = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    Dirección = models.CharField(max_length=200)
    Teléfono_contacto = models.CharField(max_length=15)
    Otros_contacto = models.EmailField(blank=True, null=True)
    email = models.CharField(blank=True,  max_length=400)
    def __str__(self):
        return self.Nombre


class Destinatario(models.Model):
    NOMBRE_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('Pasaporte', 'Pasaporte'),
    ]
    ID_Destinatario = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=255)
    tipodocumento = models.CharField(max_length=20, choices=NOMBRE_CHOICES)
    adr = models.CharField(max_length=255)
    email = models.EmailField()
    dep = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255, blank=True, null=True)
    apellidos = models.CharField(max_length=255)
    documento = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.fname


class Negocio(models.Model):
    ID_Negocio = models.AutoField(primary_key=True)
    Empresa = models.ForeignKey(EmpresaTransporteFluvial, on_delete=models.CASCADE)
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Destinatario = models.ForeignKey(Destinatario, on_delete=models.CASCADE)
    Fecha_inicio = models.DateField()
    Fecha_fin = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Negocio - ID: {self.ID_Negocio}"



    
class Pago(models.Model):
    #pagoefectivo = models.BooleanField(default=False, blank=True, null=True)
    #pagotransferencia = 
    TIPO_PAGO_CHOICES = [
        ('pago en efectivo', 'pago en efectivo'),
        ('pago por transferencia', 'pago por transferencia'),
    ]
    tipo_pago = models.CharField(max_length=100, blank=True, null=True, choices=TIPO_PAGO_CHOICES)
    valor_pagado = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    titular_cuenta = models.CharField(max_length=100, blank=True, null=True)
    numero_cuenta = models.CharField(max_length=20, blank=True, null=True)
    fecha_transaccion = models.DateField(blank=True, null=True)
            
    def __str__(self):
        return f"{self.fecha_transaccion} - ${self.valor_pagado}"


class Viaje(models.Model):   
    ID_Viaje = models.AutoField(primary_key=True)
    Guía_zarpe = models.CharField(max_length=100, verbose_name='Guía zarpe', blank=True)
    Motonave = models.ForeignKey(Motonave, on_delete=models.CASCADE, blank=True, null=True)
    Piloto = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True)
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    Remitente = models.ForeignKey(Destinatario, on_delete=models.CASCADE, related_name='viajes_remitente', blank=True, null=True)
    Destinatario = models.ForeignKey(Destinatario, on_delete=models.CASCADE, related_name='viajes_destinatario', blank=True, null=True)
    Cargas = models.ManyToManyField(Carga)  # Relación ManyToMany con Carga
    Fecha_inicio_viaje = models.DateField(default=timezone.now, blank=True, null=True)
    Fecha_fin_viaje = models.DateField(blank=True, null=True)
    Pagos = models.ForeignKey(Pago, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"Viaje - ID: {self.ID_Viaje}"
    
    def calcular_total_cargas(self):
        total_cargas = 0

        for carga in self.Cargas.all(): 
            total_cargas += float(carga.total)

        return total_cargas
    
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('ID_Viaje', 'Guía_zarpe', 'Motonave', 'Piloto', 'display_cargas', 'Fecha_inicio_viaje', 'Fecha_fin_viaje')
    list_display_links = ('ID_Viaje', 'Guía_zarpe')

    def display_cargas(self, obj):
        return ', '.join(str(carga) for carga in obj.Cargas.all())

    display_cargas.short_description = 'Cargas'


class CardDescription(models.Model):
    id_card = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Nombre', blank=True) 
    text  = models.CharField(max_length=3000, verbose_name='Texto', blank=True) 
    image  = models.CharField(max_length=500, verbose_name='Image', blank=True)
    time  = models.CharField(max_length=100, verbose_name='Tiempo', blank=True)  
    def __str__(self):
        return f"Card - ID: {self.id_card}"
    
    @classmethod
    def prepopulate(cls):
        print("Prepopulating CardDescription...")
        card = cls(
            name='Logística',
            text='Módulo para realizar el alistamiento y logística de cargas y mercancías.',
            image='images/logistica.png',
            time='9 min'
        )
        card.save()
        card = cls(
            name='Informes',
            text='Módulo para visualizar información relevante para análisis.',
            image='images/informes.png',
            time='119 min'
        )
        card.save()
        card = cls(
            name='Notificaciones',
            text='Módulo para verificar información de estado de motonaves y cargas.',
            image='images/notificaciones.png',
            time='20 min'
        )
        card.save()

class CardDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id_card', 'name', 'text', 'image', 'time')
    list_display_links = ('id_card', 'name')
    

# Registra el modelo con la clase ModelAdmin personalizada
admin.site.register(Motonave, MotonaveAdmin)
admin.site.register(Pago)
admin.site.register(EmpresaTransporteFluvial)
admin.site.register(Persona)
admin.site.register(Cargo)
admin.site.register(Carga, CargaAdmin)
admin.site.register(Cliente)
admin.site.register(Destinatario)
admin.site.register(Negocio)
admin.site.register(Viaje, ViajeAdmin)
admin.site.register(CardDescription, CardDescriptionAdmin)
admin.site.register(Departamento,DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Parameter)

def create_superuser(apps, schema_editor):
    User.objects.create_superuser(
        username='admin',
        email='jdmartinezpro@gmail.com',
        password='123'
    )




class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_superuser),
        #migrations.RunPython(load_fixture),
        migrations.RunPython(CardDescription.prepopulate)
    ]
    
def generar_cadena_aleatoria(longitud):
    letras = string.ascii_letters
    cadena_aleatoria = ''.join(random.choice(letras) for _ in range(longitud))
    return cadena_aleatoria

@receiver(pre_save, sender=Viaje)
def generar_guia_zarpe(sender, instance, **kwargs):
    if not instance.Guía_zarpe: 
        timestamp = int(time.time())    
        random_number = random.randint(1000, 9999)
        instance.Guía_zarpe =generar_cadena_aleatoria(5)+f"-{timestamp}{random_number}"