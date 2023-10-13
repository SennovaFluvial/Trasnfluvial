from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from users.models import RollUser, Menu
from users.models import Solicitud, DetalleUser, Dependencia, Permitido, Roll
from operator import itemgetter
import uuid
#import qrcode
import datetime
import zlib

#INFORMACION PERSONAL
def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        usuario = User.objects.get(username = user)
        idUser =usuario.pk
        tiposContrato = (
            "...",  
            "Termino Indefinido",
            "Prestacion de Servicios"
        )
        dependencias = Dependencia.objects.order_by('id')
        print(dependencias)
        rolljefe = RollUser.objects.filter(rollid = 2)
        print(rolljefe)
        print(idUser)
        print("---------------------");
        print(usuario.pk)
        #print(user.username)
        if request.method == "POST":
            email = request.POST['email']
            print(email)
            autorizado = Permitido.objects.filter(email = email).exists()
            print(Permitido.objects.filter(email = email))
            if autorizado is False:
                print("correo no autorizado")
                usuariodelete = User.objects.get(pk = idUser)
                usuariodelete.delete()
                context = {
                    "rolljefe": rolljefe,
                    "dependencias": dependencias,
                    "idUser":idUser,
                    "tiposContrato":tiposContrato,
                    "modal":True,
                    "response": "ErrorAutorizacion",
                    "message":'Correo no autorizado. Debe escribir al correo juan.mmorales@esap.gov.co para realizar el preregistro con los datos CEDULA Y CORREO...'
                }
                return render(request, "users/welcome.html",context)
            existe = User.objects.filter(email = email).exists()
            print(existe)
            if existe is True:
                print("correo ya existe")
                usuariodelete = User.objects.get(pk = idUser)
                usuariodelete.delete()
                context = {
                    "rolljefe": rolljefe,
                    "dependencias": dependencias,
                    "idUser":idUser,
                    "tiposContrato":tiposContrato,
                    "modal":True,
                    "response": "ErrorExiste",
                    "message":'Este correo ya esta registrado. Debe escribir al correo juan.mmorales@esap.gov.co para realizar el preregistro con los datos CEDULA Y CORREO...'
                }
                return render(request, "users/welcome.html",context)
            
            print("entró al post")
            dep = request.POST.get('dependencia')
            depens = Dependencia.objects.get(id = dep)
            usuario.email = request.POST['email']
            nuevo = DetalleUser(
                idUser=usuario,
                tipoContrato=request.POST['tipoContrato'],
                idjefe=request.POST.get('jefeInmediato'),
                telefono=request.POST['telefono'],
                direccion=request.POST['direccion'],
                cedula=request.POST['cedula'],
                idDependencia=depens
            )
            usuario.save()
            nuevo.save()
            context = {
                "modal":True,
                "response": "Success",
                "message":'Se guardó la información. Ahora puede iniciar sesion.'
            } 
            return render(request, "users/login.html", context)
        # En otro caso redireccionamos al login
        context = {
                "rolljefe": rolljefe,
                "dependencias": dependencias,
                "idUser":idUser,
                "tiposContrato":tiposContrato
            } 
        return render(request, "users/welcome.html",context)
    return redirect('/login')


#MENU PARA LOS TRES ROLES (TRAMITADOR, AUTORIZADOR, TELNTO HUMANO)
def menu(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        print("_____1____________")
        print(id_roll)
        context = {
            "user": user,
            "Roll": roll,
            "menus": menus
        }
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')


#PROCESOS DEL TRAMITADOR________________________________________________________________________________________
def enviarSolicitud(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        print("_______2__________")
        print(id_roll)
        context = {
            "user": user,
            "Roll": roll,
            "menus": menus
        }
        
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def newsolicitud(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        tiposDiligencia = (
            "...",  
            "Reunion",
            "Documentacion",
            "Servicios generales",
            "Solicitudes",
            "Revision de espacios",
            "Supervisar",
            "Otra"
        )
        print("______3___________")
        print(id_roll)
        #inicio de dashboard
        if request.method == "POST":
            print("possssssssssssssssss")
            fecha = request.POST['fechaIngreso']
            horaIngreso = request.POST['horaIngreso']
            horaSalida = request.POST['horaSalida']
            diligencia = request.POST['diligencia']
            justificacionsoli = request.POST['justificacion']
            print("____")
            detalle = DetalleUser.objects.get(idUser = idUser)
            nueva = Solicitud(estado='Solicitado', 
                            fechaIngreso=fecha, 
                            horaIngreso=horaIngreso,
                            horaSalida=horaSalida, 
                            diligencia=diligencia, 
                            justificacion=justificacionsoli,
                            idUser= usuario,
                            nombres = usuario.first_name,
                            apellidos = usuario.last_name,
                            correo = usuario.email,
                            cedula = detalle.cedula,
                            dependencia = detalle.idDependencia,
                            jefeInmediato =detalle.idjefe,
                            fechaModificacion = datetime.date.today())
            nueva.save()
            context = {
                "usuario": usuario,
                "Roll": roll,
                "menus": menus,
                "modal":True,
                "response": "Success",
                "message":'Solicitud enviada.'
            } 
            return render(request, "users/menu.html",context)
        #fin de dashboard
        context = {
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":1,
            "tiposDiligencia":tiposDiligencia,

        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def solicitudes(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        solicitudes = Solicitud.objects.filter(idUser = idUser).order_by('-fechaModificacion')
        solicitudaux = Solicitud.objects.order_by('-fechaIngreso')
        print(solicitudaux)
        print("_________5________")
        print(id_roll)
        print(idUser)
        print(solicitudes)
        #inicio de dashboard

        #fin de dashboard
        context = {
            "solicitudes": solicitudes,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":2
        }        
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def revisarSolic(request, id_solicitud):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        print("<<<<<<"+str(id_solicitud)+">>>>>>>")

        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        solicitud = Solicitud.objects.get(pk = id_solicitud)
        usuarioJefe=User.objects.get(pk=solicitud.jefeInmediato)
        dependencia = Dependencia.objects.get(pk = solicitud.dependencia.id)
        
        print("______17___________")
        print(solicitud)
        #inicio de dashboard
        print(solicitud.observaciontalentoH)
        #if request.method == "GET":
        #       request.method = 'POST'
        
        #fin de dashboard
        context = {
            "solicitud": solicitud,
            "dependencia": dependencia,
            "usuarioJefe":usuarioJefe,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":14
        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def corregirSolicitud(request, id_solicitud):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        print("<<<<<<"+str(id_solicitud)+">>>>>>>")

        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        tiposDiligencia = (
            "...",  
            "Reunion",
            "Documentacion",
            "Servicios generales",
            "Solicitudes",
            "Revision de espacios",
            "Supervisar",
            "Otra"
        )
        solicitud = Solicitud.objects.get(idUser = idUser, pk = id_solicitud)
        usuarioJefe=User.objects.get(pk=solicitud.jefeInmediato)
        dependencia = Dependencia.objects.get(pk = solicitud.dependencia.id)
        
        print("______18___________")
        print(solicitud)
        #inicio de dashboard
        print(request.method)
        if request.method == "POST":
            print("possssssssssssssssss")
            fecha = request.POST['fechaIngreso']
            horaIngreso = request.POST['horaIngreso']
            horaSalida = request.POST['horaSalida']
            diligencia = request.POST['tiposDiligencia']
            justificacionsoli = request.POST['justificacion']
            print("____")
            detalle = DetalleUser.objects.get(idUser = idUser)
            solicitud.estado='Solicitado'
            solicitud.fechaIngreso=fecha
            solicitud.horaIngreso=horaIngreso
            solicitud.horaSalida=horaSalida
            solicitud.diligencia=diligencia
            solicitud.justificacion=justificacionsoli
            solicitud.fechaModificacion = datetime.date.today()
            solicitud.save()
            context = {
                "usuario": usuario,
                "Roll": roll,
                "menus": menus,
                "modal":True,
                "response": "Success",
                "message":'Actualizado correctamente.'
            } 
            return render(request, "users/menu.html",context)
        #fin de dashboard
        context = {
            "solicitud": solicitud,
            "dependencia": dependencia,
            "usuarioJefe":usuarioJefe,
            "usuario": usuario,
            "tiposDiligencia":tiposDiligencia,
            "Roll": roll,
            "menus": menus,
            "dashboard":15
        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def borrarSolicitud(request, id_solicitud):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        print("<<<<<<"+str(id_solicitud)+">>>>>>>")

        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        solicitud = Solicitud.objects.get(pk = id_solicitud)
        solicitud.delete()
        
        print("______20___________")
        print(solicitud)
        #inicio de dashboard
        print(request.method)
        #fin de dashboard
        context = {
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "modal":True,
            "response": "Error",
            "message":'Eliminado correctamente.'
        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')


#PROCESOS DEL AUTORIZADOR________________________________________________________________________________________
def bandejasolicitudes(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        solicitudes = Solicitud.objects.filter(jefeInmediato = idUser, estado = 'Solicitado').order_by('-fechaModificacion')
        print("_________6________")
        print(id_roll)
        print(idUser)
        print(solicitudes)
        #inicio de dashboard

        #fin de dashboard
        context = {
            "solicitudes": solicitudes,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":3
        }        
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def revisarSolicitud(request,home_, id_solicitud):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        print("<<<<<<"+str(id_solicitud)+">>>>>>>")

        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        solicitud = Solicitud.objects.get(jefeInmediato = idUser, pk = id_solicitud)
        usuarioJefe=User.objects.get(pk=solicitud.jefeInmediato)
        dependencia = Dependencia.objects.get(pk = solicitud.dependencia.id)
        
        print("______7___________")
        print(solicitud)
        #inicio de dashboard
        print(request.method)
        #if request.method == "GET":
        #       request.method = 'POST'
        if request.method == "POST":
            print(request.method)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>"+request.POST['estado'])
            #observacion = request.POST['observacionjefeI']
            solicitud.observacionjefeI = request.POST['observacionjefeI']
            solicitud.estado = request.POST['estado']
            solicitud.fechaModificacion = datetime.date.today()
            solicitud.save()
            context = {
                "solicitud": solicitud,
                "dependencia": dependencia,
                "usuarioJefe":usuarioJefe,
                "usuario": usuario,
                "Roll": roll,
                "menus": menus,
                "modal":True,
                "response": solicitud.estado
            } 
            return render(request, "users/menu.html",context)
        #fin de dashboard
        context = {
            "solicitud": solicitud,
            "dependencia": dependencia,
            "usuarioJefe":usuarioJefe,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":4
        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def historialSolicitudes(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        solicitudes = Solicitud.objects.filter(jefeInmediato = idUser).order_by('-fechaModificacion')

        #solicitudes = Solicitud.objects.order_by('fechaIngreso')
        print("_________8________")
        print(id_roll)
        print(idUser)
        print(solicitudes)
        #inicio de dashboard

        #fin de dashboard
        context = {
            "solicitudes": solicitudes,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":5
        }        
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def verSolicitud(request, id_solicitud):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        print("<<<<<<"+str(id_solicitud)+">>>>>>>")

        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        solicitud = Solicitud.objects.get(jefeInmediato = idUser, pk = id_solicitud)
        usuarioJefe=User.objects.get(pk=solicitud.jefeInmediato)
        dependencia = Dependencia.objects.get(pk = solicitud.dependencia.id)
        
        print("______9___________")
        print(solicitud)
        #inicio de dashboard
        print(request.method)
        
        #fin de dashboard
        context = {
            "solicitud": solicitud,
            "dependencia": dependencia,
            "usuarioJefe":usuarioJefe,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":6
        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def reporteSolicitudes(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        fecha_reporte = request.POST.get('fechaReporte')

        solicitudes = Solicitud.objects.filter(jefeInmediato = idUser, fechaIngreso = fecha_reporte).order_by('-fechaModificacion')
        #solicitudes = Solicitud.objects.filter(jefeInmediato = idUser).order_by('-fechaModificacion')
        print("_________10________")
        print(id_roll)
        print(idUser)
        print(solicitudes)
        print(fecha_reporte)
        #inicio de dashboard

        #fin de dashboard
        context = {
            "solicitudes": solicitudes,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":7
        }        
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def verSolicitudRep(request, id_solicitud):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        print("<<<<<<"+str(id_solicitud)+">>>>>>>")

        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        solicitud = Solicitud.objects.get(jefeInmediato = idUser, pk = id_solicitud)
        usuarioJefe=User.objects.get(pk=solicitud.jefeInmediato)
        dependencia = Dependencia.objects.get(pk = solicitud.dependencia.id)
        
        print("______11___________")
        print(solicitud)
        #inicio de dashboard
        print(solicitud.estado)
        
        #fin de dashboard
        context = {
            "solicitud": solicitud,
            "dependencia": dependencia,
            "usuarioJefe":usuarioJefe,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":8
        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def revisarSolicitudRep(request, id_solicitud):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        print("<<<<<<"+str(id_solicitud)+">>>>>>>")

        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        solicitud = Solicitud.objects.get(jefeInmediato = idUser, pk = id_solicitud)
        usuarioJefe=User.objects.get(pk=solicitud.jefeInmediato)
        dependencia = Dependencia.objects.get(pk = solicitud.dependencia.id)
        
        print("______12___________")
        print(solicitud)
        #inicio de dashboard
        print(request.method)
        #if request.method == "GET":
        #       request.method = 'POST'
        if request.method == "POST":
            print(request.method)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>"+request.POST['estado'])
            #observacion = request.POST['observacionjefeI']
            solicitud.observacionjefeI = request.POST['observacionjefeI']
            solicitud.estado = request.POST['estado']
            solicitud.fechaModificacion = datetime.date.today()
            solicitud.save()
            context = {
                "solicitud": solicitud,
                "dependencia": dependencia,
                "usuarioJefe":usuarioJefe,
                "usuario": usuario,
                "Roll": roll,
                "menus": menus,
                "modal":True,
                "response": solicitud.estado
            } 
            return render(request, "users/menu.html",context)
        #fin de dashboard
        context = {
            "solicitud": solicitud,
            "dependencia": dependencia,
            "usuarioJefe":usuarioJefe,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":9,
        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')


#PROCESOS DE TALENTO HUMANO________________________________________________________________________________________
def bandejaSolicitudes(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        solicitudes = Solicitud.objects.filter(estado = 'Aprobado').order_by('-fechaModificacion')
        print("_________13________")
        print(id_roll)
        print(idUser)
        print(solicitudes)
        #inicio de dashboard
        today = datetime.date.today()
        print(today)

        #fin de dashboard
        context = {
            "solicitudes": solicitudes,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":10
        }        
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def revisarSolicitudByTalento(request, id_solicitud):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        print("<<<<<<"+str(id_solicitud)+">>>>>>>")

        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        solicitud = Solicitud.objects.get(pk = id_solicitud)
        usuarioJefe=User.objects.get(pk=solicitud.jefeInmediato)
        dependencia = Dependencia.objects.get(pk = solicitud.dependencia.id)
        
        print("______14___________")
        print(solicitud)
        #inicio de dashboard
        print(request.method)
        if request.method == "POST":
            print(request.method)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>"+request.POST['estado'])
            #observacion = request.POST['observacionjefeI']
            solicitud.observaciontalentoH = request.POST['observaciontalentoH']
            solicitud.estado = request.POST['estado']
            token = uuid.uuid1()
            print(token.bytes)
            print(zlib.crc32(token.bytes))
            solicitud.token = zlib.crc32(token.bytes)
            solicitud.fechaModificacion = datetime.date.today()
            solicitud.save()
            context = {
                "solicitud": solicitud,
                "dependencia": dependencia,
                "usuarioJefe":usuarioJefe,
                "usuario": usuario,
                "Roll": roll,
                "menus": menus,
                "modal":True,
                "response": solicitud.estado
            } 
            return render(request, "users/menu.html",context)
        #fin de dashboard
        context = {
            "solicitud": solicitud,
            "dependencia": dependencia,
            "usuarioJefe":usuarioJefe,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":11,
        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def solicitudesAprobadas(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        solicitudes = Solicitud.objects.all().order_by('-fechaIngreso')
        print("_________15________")
        print(id_roll)
        print(idUser)
        print(solicitudes)
        #inicio de dashboard

        #fin de dashboard
        context = {
            "solicitudes": solicitudes,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":12
        }        
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def verSolicitudAprobada(request, id_solicitud):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        print("<<<<<<"+str(id_solicitud)+">>>>>>>")

        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        solicitud = Solicitud.objects.get(pk = id_solicitud)
        usuarioJefe=User.objects.get(pk=solicitud.jefeInmediato)
        dependencia = Dependencia.objects.get(pk = solicitud.dependencia.id)
        
        print("______16___________")
        print(solicitud)
        #inicio de dashboard
        print(solicitud.estado)
        
        #fin de dashboard
        context = {
            "solicitud": solicitud,
            "dependencia": dependencia,
            "usuarioJefe":usuarioJefe,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":13
        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')


#VERIFICACION_________________________________________________________________________________________________
def solicitudesVerificador(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        fecha_reporte = request.POST.get('fechaReporte')

        solicitudes = Solicitud.objects.filter(estado = 'AprobadoTH', fechaIngreso = fecha_reporte).order_by('fechaIngreso')
        print("_________VERIFICAR________")
        print(id_roll)
        print(idUser)
        print(solicitudes)
        print(fecha_reporte)
        #inicio de dashboard

        #fin de dashboard
        context = {
            "solicitudes": solicitudes,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":16
        }        
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def versolicitudVerificada(request, id_solicitud):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        print("<<<<<<"+str(id_solicitud)+">>>>>>>")

        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        solicitud = Solicitud.objects.get(pk = id_solicitud)
        usuarioJefe=User.objects.get(pk=solicitud.jefeInmediato)
        dependencia = Dependencia.objects.get(pk = solicitud.dependencia.id)
        
        print("______VERIFICAR________")
        print(solicitud)
        #inicio de dashboard
        print(solicitud.estado)
        #fin de dashboard
        if request.method == "POST":
            solicitud.horaEntrada = request.POST['horaEntrada']
            solicitud.temperatura = request.POST['temperatura']
            solicitud.estado = 'Verificado'
            solicitud.save()
            context = {
                "usuario": usuario,
                "Roll": roll,
                "menus": menus,
                "modal":True,
                "response": 'Verificado'
            } 
            return render(request, "users/menu.html",context)
        context = {
            "solicitud": solicitud,
            "dependencia": dependencia,
            "usuarioJefe":usuarioJefe,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":17
        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def solicitudesVerificadas(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        
        fecha_reporte = request.POST.get('fechaReporte')

        solicitudes = Solicitud.objects.filter(estado = 'Verificado').order_by('fechaModificacion')
        print("_________VERIFICAR________")
        print(id_roll)
        print(idUser)
        print(solicitudes)
        print(fecha_reporte)
        #inicio de dashboard

        #fin de dashboard
        context = {
            "solicitudes": solicitudes,
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":26
        }        
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')

def verificado(request):
    print(request.method)
    token1 = request.POST.get('token')
    print(token1)
    if request.method == "POST":
        print(request.method)
        token1 = request.POST.get('token')
        verifiExiste = Solicitud.objects.filter(token = token1).exists()
        
        if verifiExiste is False:
            print("Token no Existe")
            context = {
                "dashboard":23
            }
            return render(request, "users/verificado.html", context)
        
        solicitud = Solicitud.objects.get(token = token1)
        dependencia = Dependencia.objects.get(pk = solicitud.dependencia)
        
        print(token1)
        print(solicitud)
        context = {
            "solicitud": solicitud,
            "dependencia": dependencia,
            "dashboard":20
        }
        return render(request, "users/verificado.html", context)
    context = {
        "dashboard":24
    }
    return render(request, "users/verificado.html", context)

def verificado2(request, token1):
    print(request.method)
    #token1 = request.POST.get('token')
    print(token1)
    print(request.method)
    #token1 = request.POST.get('token')
    solicitud = Solicitud.objects.get(token = token1)
    print(token1)
    print(solicitud)
    context = {
        "solicitud": solicitud,
        "dashboard":21
    }
    return render(request, "users/verificado.html", context)


#REGISTRAR USUARIO NUEVO_________________________________________________________________________________________________
def registrarUsuario(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        rolljefe = RollUser.objects.filter(rollid = 2)
        #jefes = User.objects.filter(pk = rolljefe.userid)
        print("Formato registro nuevo usuario")
        tiposContrato = (
            "...",  
            "Termino Indefinido",
            "Prestacion de Servicios"
        )
        dependencias = Dependencia.objects.order_by('id')
        rolls = Roll.objects.order_by('pk')
        if request.method == "POST":
            newPassW1 = request.POST['new_password1']
            newPassW2 = request.POST['new_password2']
            nUsuario = request.POST['username']
            primerNombre = request.POST['first_name']
            segundoNombre = request.POST['last_name']
            correo = request.POST['email']
            cedula = request.POST['cedula']
            tipoContratoSel = request.POST['tipoContrato']
            jefeInmediato = request.POST['jefeInmediato']
            telefono = request.POST['telefono']
            direccion = request.POST['direccion']
            depen = request.POST['dependencia']
            roll = request.POST['rolls']
            existeRoll = Roll.objects.filter(id = roll).exists()
            if existeRoll is False:
                print('no eligio un rol')
                context = {
                    "tiposContrato": tiposContrato,
                    "dependencias": dependencias,
                    "rolls": rolls,
                    "rolljefe": rolljefe,
                    "menus": menus,
                    "dashboard":18,
                    "modal":True,
                    "response": 'elegirRoll'
                }
                return render(request, "users/menu.html",context)
            existeDepen = Dependencia.objects.filter(id = depen).exists()
            if existeDepen is False:
                print('no eligio una dependencia')
                context = {
                    "tiposContrato": tiposContrato,
                    "dependencias": dependencias,
                    "rolls": rolls,
                    "rolljefe": rolljefe,
                    "menus": menus,
                    "dashboard":18,
                    "modal":True,
                    "response": 'elegirDependencia'
                }
                return render(request, "users/menu.html",context)
            dependencia = Dependencia.objects.get(id = depen)
            usuarioRoll = Roll.objects.get(id = roll)
            usuarioUnico = User.objects.filter(username = nUsuario).exists()
            if usuarioUnico is True :
                print('Existe un usuario con el mismo Username')
                context = {
                    "tiposContrato": tiposContrato,
                    "dependencias": dependencias,
                    "rolls": rolls,
                    "rolljefe": rolljefe,
                    "menus": menus,
                    "dashboard":18,
                    "modal":True,
                    "response": 'Existeusuario'
                }
                return render(request, "users/menu.html",context)
            if newPassW1 != newPassW2 :
                print('la contraseña no coincide')
                context = {
                    "tiposContrato": tiposContrato,
                    "dependencias": dependencias,
                    "rolls": rolls,
                    "rolljefe": rolljefe,
                    "menus": menus,
                    "dashboard":18,
                    "modal":True,
                    "response": 'passwordDif'
                }
                return render(request, "users/menu.html",context)
            if newPassW1 == newPassW2:
                print('se creara el usuario y lo guardara')
                nuevoUsuario = User(
                    username = nUsuario,
                    first_name = primerNombre,
                    last_name = segundoNombre,
                    email = correo,
                    password = '0',
                    is_superuser = 1,
                    is_staff = 1,
                    is_active = 1,
                )
                nuevoUsuario.save()
                id_nuevoUsuario = User.objects.get(username = nUsuario)
                u = User.objects.get(id=id_nuevoUsuario.id)
                u.set_password(newPassW1)
                u.save()
                nuevoDetalle = DetalleUser(
                    idUser = id_nuevoUsuario,
                    idDependencia = dependencia,
                    tipoContrato = tipoContratoSel,
                    idjefe = jefeInmediato,
                    telefono = telefono,
                    direccion = direccion,
                    cedula = cedula
                )
                nuevoDetalle.save()
                nuevoRoll = RollUser(
                    userid = id_nuevoUsuario,
                    rollid = usuarioRoll
                )
                nuevoRoll.save()
                context = {
                    "tiposContrato": tiposContrato,
                    "dependencias": dependencias,
                    "rolls": rolls,
                    "rolljefe": rolljefe,
                    "menus": menus,
                    "dashboard":18,
                    "modal":True,
                    "response": 'newUsuarioOK'
                }
                return render(request, "users/menu.html",context)
            context = {
                "tiposContrato": tiposContrato,
                "dependencias": dependencias,
                "rolls": rolls,
                "rolljefe": rolljefe,
                "menus": menus,
                "usuario": usuario,
                "Roll": roll,
                "menus": menus
            } 
            return render(request, "users/menu.html",context)
        context = {
            "tiposContrato": tiposContrato,
            "dependencias": dependencias,
            "rolls": rolls,
            "rolljefe": rolljefe,
            "menus": menus,
            "dashboard":18
        } 
        return render(request, "users/menu.html",context)
    return redirect('/login')

def usuariosRegistrados(request):
    if request.user.is_authenticated:
        user = request.user
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        usuarios = User.objects.order_by('pk')
        #rollUsuario = RollUser.objects.get(userid = usuarios.pk)
        #depUsuario = DetalleUser.objects.get(idUser = usuarios.pk)
        context = {
            "usuarios": usuarios,
            "usuario": usuario,
            "menus": menus,
            "dashboard":19
        }
        return render(request, "users/menu.html",context)
    return redirect('/login')

def verDatosUsuario(request, id_usuario):
    if request.user.is_authenticated:
        user = request.user
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        usuario = User.objects.get(id = id_usuario)
        detalle = DetalleUser.objects.get(idUser = id_usuario)
        rol = RollUser.objects.get(userid = id_usuario)
        auxJefe = detalle.idjefe
        if detalle.idjefe == -1:
            context = {
            "auxJefe": auxJefe,
            "usuario": usuario,
            "detalle": detalle,
            "rol": rol,
            "menus": menus,
            "dashboard":25
            }
            return render(request, "users/menu.html",context)
        jefe = User.objects.get(id = detalle.idjefe)
        print(usuario)
        print(detalle)
        print(rol)
        context = {
            "auxJefe": auxJefe,
            "usuario": usuario,
            "detalle": detalle,
            "rol": rol,
            "jefe": jefe,
            "menus": menus,
            "dashboard":25
        }
        return render(request, "users/menu.html",context)
    return redirect('/login')


#LOGIN, LOGOUT, REGISTRO Y CAMBIAR CONTRASEÑA
def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
    
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()
            print(user.username)

            # Si existe el usuario
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/welcome')

    # Si queremos borramos los campos de ayuda
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/register.html", {'form': form})

def login(request):    
    return render(request, "users/index.html")

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

def cambiarContraseña(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        idUser = User.objects.get(username = user).pk
        usuario=User.objects.get(username=user)
        roll = RollUser.objects.get(userid = idUser)
        id_roll = roll.rollid.pk
        menus = Menu.objects.filter(idRoll = id_roll)
        print("______Cambio contraseña___________")
        print(idUser)
        print(usuario)
        #inicio de dashboard
        if request.method == "POST":
            print("posssssssssssssssssst")
            oldPassW = request.POST['old_password']
            newPassW1 = request.POST['new_password1']
            newPassW2 = request.POST['new_password2']
            autentica = authenticate(username=usuario, password=oldPassW) #verificar si el password actual coincide
            if autentica is None:
                print('la contraseña actual no coincide')
                context = {
                    "dashboard":22,
                    "modal":True,
                    "response": 'Contraseñaactual'
                }
                return render(request, "users/menu.html",context)
            if oldPassW==newPassW1 or oldPassW==newPassW2 :
                print('la nueva contraseña es igual a la antigua')
                context = {
                    "dashboard":22,
                    "modal":True,
                    "response": 'Contraseñaigual'
                }
                return render(request, "users/menu.html",context)
            if newPassW1 != newPassW2 :
                print('la nueva contraseña no coincide')
                context = {
                    "dashboard":22,
                    "modal":True,
                    "response": 'Contraseñadif'
                }
                return render(request, "users/menu.html",context)
            if newPassW1 == newPassW2 and oldPassW != newPassW1 and oldPassW != newPassW2 :
                print('se realizó el cambio de contraseña')
                u = User.objects.get(username=user)
                u.set_password(newPassW1)
                u.save()
                context = {
                    "usuario": usuario,
                    "Roll": roll,
                    "menus": menus,
                    "modal":True,
                    "response": 'Contraseñaok'
                }
                return render(request, "users/menu.html",context)
            print(oldPassW)
            print(newPassW1)
            print(newPassW2)
            context = {
                "usuario": usuario,
                "Roll": roll,
                "menus": menus,
            } 
            return render(request, "users/menu.html",context)


        #fin de dashboard
        context = {
            "usuario": usuario,
            "Roll": roll,
            "menus": menus,
            "dashboard":22,

        } 
        return render(request, "users/menu.html",context)
    # En otro caso redireccionamos al login
    return redirect('/login')