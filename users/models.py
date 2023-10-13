from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Permitido(models.Model):
    cedula = models.CharField(max_length=70)
    email = models.EmailField(max_length=200)
    class Meta:
        db_table = "Permitido"

class Dependencia(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=70)
    class Meta:
        db_table = "dependencia"

class DetalleUser(models.Model):
    idUser = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    idDependencia = models.ForeignKey(Dependencia,on_delete=models.CASCADE)
    tipoContrato = models.CharField(max_length=70)
    idjefe =models.BigIntegerField()
    telefono = models.CharField(max_length=70)
    direccion = models.CharField(max_length=70)
    cedula = models.CharField(max_length=70)
    class Meta:
        db_table = "detalle_usuario"

class Roll(models.Model):    
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=70)
    class Meta:
        db_table = "roll"

class RollUser(models.Model):    
    userid = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    rollid = models.ForeignKey(Roll, on_delete=models.CASCADE)
    class Meta:
        db_table = "roll_user"

class Menu(models.Model):
    id = models.IntegerField(primary_key=True)
    idRoll = models.ForeignKey(Roll, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=70)
    Ruta = models.CharField(max_length=70)
    Desccripcion = models.CharField(max_length=70)
    Imagen = models.CharField(max_length=70)
    idPadre = models.IntegerField('idPadre', default=False)
    Negrilla = models.BooleanField(default=False)
    Subrayado = models.BooleanField(default=False)
    class Meta:
        db_table = "menu"

class Solicitud(models.Model):
    idUser = models.ForeignKey(User,on_delete=models.CASCADE)
    nombres = models.CharField(max_length=70)
    apellidos = models.CharField(max_length=70)
    correo = models.EmailField(max_length=200)
    cedula = models.CharField(max_length=70)
    dependencia = models.ForeignKey(Dependencia,on_delete=models.CASCADE)
    jefeInmediato = models.CharField(max_length=70)
    fechaIngreso = models.DateField(auto_now=False, auto_now_add=False,  blank=True, null=True)
    horaIngreso = models.TimeField(auto_now=False, auto_now_add=False,  blank=True, null=True)
    horaSalida = models.TimeField(auto_now=False, auto_now_add=False,  blank=True, null=True)
    diligencia = models.CharField(max_length=100)
    justificacion = models.CharField(max_length=900,  blank=True, null=True)
    token = models.CharField(max_length=70)
    estado = models.CharField(max_length=70)
    documento = models.CharField(max_length=70)
    observacionjefeI = models.CharField(max_length=900, blank=True, null=True)
    observaciontalentoH = models.CharField(max_length=900, blank=True, null=True)
    fechaModificacion = models.DateField(auto_now=False, auto_now_add=False,  blank=True, null=True)
    temperatura = models.CharField(max_length=70, null=True)
    horaEntrada = models.TimeField(auto_now=False, auto_now_add=False,  blank=True, null=True)