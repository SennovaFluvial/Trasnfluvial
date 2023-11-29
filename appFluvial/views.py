from decimal import Decimal
import decimal
from django.forms import model_to_dict
from django.utils import timezone
import json
import uuid
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import CardDescription, Carga, Destinatario, Viaje

from .forms import Card1DestinatarioForm, Card1RemitenteForm, CargaForm
from .models import Departamento, Municipio
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

# def home(request):
#    return render(request, 'home.html')

def index(request):
    cards = CardDescription.objects.all()
    return render(request, 'index.html', {'cards': cards})

class MiLoginView(LoginView):
    template_name = 'appFluvial/login.html'  # Puedes personalizar tu plantilla de inicio de sesión
    success_url = reverse_lazy('logistica')  # Redirige a esta vista después de iniciar sesión

#@login_required
def logistica(request):
    print("---remitente---")     
    if request.method == 'POST':
        form = Card1RemitenteForm(request.POST)

        if form.is_valid():
            # Obtener la cédula del formulario
            cedula = form.cleaned_data['documento']

            # Intentar obtener un Destinatario existente con la misma cédula
            destinatario_existente = Destinatario.objects.filter(documento=cedula).first()

            # Actualizar los campos existentes con los valores del formulario
            if destinatario_existente:
                form_instance = form.save(commit=False)
                destinatario_existente.fname = form_instance.fname
                destinatario_existente.tipodocumento = form_instance.tipodocumento
                destinatario_existente.adr = form_instance.adr
                destinatario_existente.email = form_instance.email
                destinatario_existente.dep = form_instance.dep
                destinatario_existente.empresa = form_instance.empresa
                destinatario_existente.apellidos = form_instance.apellidos
                destinatario_existente.telefono = form_instance.telefono
                destinatario_existente.city = form_instance.city
                destinatario_existente.save()
                
                destinatario_json = json.dumps({
                    'fname': destinatario_existente.fname,
                    'tipodocumento': destinatario_existente.tipodocumento,
                    'adr': destinatario_existente.adr,
                    'email': destinatario_existente.email,
                    'dep': destinatario_existente.dep,
                    'empresa': destinatario_existente.empresa,
                    'apellidos': destinatario_existente.apellidos,
                    'documento': destinatario_existente.documento,
                    'telefono': destinatario_existente.telefono,
                    'city': destinatario_existente.city,
                })                
                
                request.session['remitente_info'] = destinatario_json
            else:
                # Si no existe, guardar como un nuevo registro
                # Si no existe, guardar como un nuevo registro
                new_destinatario = form.save()
                messages.success(request, 'Remitente agregado exitosamente.')

                # Serializar el objeto del destinatario a JSON y guardarlo en la sesión
                remitente_json = json.dumps({
                    'fname': new_destinatario.fname,
                    'tipodocumento': new_destinatario.tipodocumento,
                    'adr': new_destinatario.adr,
                    'email': new_destinatario.email,
                    'dep': new_destinatario.dep,
                    'empresa': new_destinatario.empresa,
                    'apellidos': new_destinatario.apellidos,
                    'documento': new_destinatario.documento,
                    'telefono': new_destinatario.telefono,
                    'city': new_destinatario.city,
                })

                request.session['remitente_info'] = remitente_json

            return redirect('../../card/1/destinatario')
        else:
            print("formulario invalido..........")
            print(form.errors)
    else:
        form = Card1RemitenteForm()
        
    return render(request, 'card1.html', {'form': form})

def obtener_municipios(request):
    departamento_id = request.GET.get('departamento_id')

    if departamento_id:
        municipios = Municipio.objects.filter(departamento__id=departamento_id)
        municipios_data = {'municipios': {}}
        for municipio in municipios:
            municipios_data['municipios'][municipio.id] = municipio.nombre
        print(municipios_data)
        return JsonResponse(municipios_data)
    else:
        return JsonResponse({'municipios': {}})

def obtener_destinatario_por_cedula(request):
    if request.method == 'GET':
        cedula = request.GET.get('cedula', None)
        if cedula:
            try:
                destinatario = Destinatario.objects.get(documento=cedula)
                data = {
                    'fname': destinatario.fname,
                    'tipodocumento': destinatario.tipodocumento,
                    'adr': destinatario.adr,
                    'email': destinatario.email,
                    'dep': destinatario.dep,
                    'empresa': destinatario.empresa,
                    'apellidos': destinatario.apellidos,
                    'telefono': destinatario.telefono,
                    'city': destinatario.city,
                }
                return JsonResponse(data)
            except Destinatario.DoesNotExist:
                # Si no se encuentra el destinatario, devolver un objeto vacío
                return JsonResponse({})
        else:
            # Si no se proporciona la cédula, devolver un objeto vacío
            return JsonResponse({})
    else:
        # Si no es una solicitud GET, devolver un objeto vacío
        return JsonResponse({})
  
def logistica_destinatario(request):    
    
    print("---destinatario---")     
    remitente_info = request.session.get('remitente_info', None)
    
    print(remitente_info)
    
    if remitente_info:
        remitente_info = json.loads(remitente_info)
        print(remitente_info)
    print("---destinatario---1111") 
    if request.method == 'POST':
        form = Card1DestinatarioForm(request.POST)
        print("---destinatario---2") 
        if form.is_valid():
            cedula = form.cleaned_data['documento']
            destinatario_existente = Destinatario.objects.filter(documento=cedula).first()
            if destinatario_existente:
                form_instance = form.save(commit=False)
                destinatario_existente.fname = form_instance.fname
                destinatario_existente.tipodocumento = form_instance.tipodocumento
                destinatario_existente.adr = form_instance.adr
                destinatario_existente.email = form_instance.email
                destinatario_existente.dep = form_instance.dep
                destinatario_existente.empresa = form_instance.empresa
                destinatario_existente.apellidos = form_instance.apellidos
                destinatario_existente.telefono = form_instance.telefono
                destinatario_existente.city = form_instance.city
                destinatario_existente.save()
                
                destinatario_json = json.dumps({
                    'fname': destinatario_existente.fname,
                    'tipodocumento': destinatario_existente.tipodocumento,
                    'adr': destinatario_existente.adr,
                    'email': destinatario_existente.email,
                    'dep': destinatario_existente.dep,
                    'empresa': destinatario_existente.empresa,
                    'apellidos': destinatario_existente.apellidos,
                    'documento': destinatario_existente.documento,
                    'telefono': destinatario_existente.telefono,
                    'city': destinatario_existente.city,
                })
                
                request.session['remitente_info'] = remitente_info
                request.session['destinatario_json'] = destinatario_json             
                
            else:
                # Si no existe, guardar como un nuevo registro
                # Si no existe, guardar como un nuevo registro
                destinatario_existente = form.save()
                messages.success(request, 'Destinatario agregado exitosamente.')

                # Serializar el objeto del destinatario a JSON y guardarlo en la sesión
                destinatario_json = json.dumps({
                    'fname': destinatario_existente.fname,
                    'tipodocumento': destinatario_existente.tipodocumento,
                    'adr': destinatario_existente.adr,
                    'email': destinatario_existente.email,
                    'dep': destinatario_existente.dep,
                    'empresa': destinatario_existente.empresa,
                    'apellidos': destinatario_existente.apellidos,
                    'documento': destinatario_existente.documento,
                    'telefono': destinatario_existente.telefono,
                    'city': destinatario_existente.city,
                })

                request.session['remitente_info'] = remitente_info
                request.session['destinatario_json'] = destinatario_json
                
                
            remite = Destinatario.objects.get(documento=remitente_info['documento'])
            
            viaje = Viaje.objects.create(Guía_zarpe=str(uuid.uuid4()),
                                         Remitente=remite, 
                                         Destinatario= destinatario_existente,
                                         Fecha_inicio_viaje=timezone.now())
            
            viaje_data = {
                'ID_Viaje': viaje.ID_Viaje,
                'Guía_zarpe': viaje.Guía_zarpe,
                'Remitente': {
                    'fname': viaje.Remitente.fname,
                    'tipodocumento': viaje.Remitente.tipodocumento,
                    'adr': viaje.Remitente.adr,
                    'email': viaje.Remitente.email,
                    'dep': viaje.Remitente.dep,
                    'empresa': viaje.Remitente.empresa,
                    'apellidos': viaje.Remitente.apellidos,
                    'documento': viaje.Remitente.documento,
                    'telefono': viaje.Remitente.telefono,
                    'city': viaje.Remitente.city,
                },
                'Destinatario': {
                    'fname': viaje.Destinatario.fname,
                    'tipodocumento': viaje.Destinatario.tipodocumento,
                    'adr': viaje.Destinatario.adr,
                    'email': viaje.Destinatario.email,
                    'dep': viaje.Destinatario.dep,
                    'empresa': viaje.Destinatario.empresa,
                    'apellidos': viaje.Destinatario.apellidos,
                    'documento': viaje.Destinatario.documento,
                    'telefono': viaje.Destinatario.telefono,
                    'city': viaje.Destinatario.city,
                },
                'Fecha_inicio_viaje': viaje.Fecha_inicio_viaje.isoformat() if viaje.Fecha_inicio_viaje else None,
                'Fecha_fin_viaje': viaje.Fecha_fin_viaje.isoformat() if viaje.Fecha_fin_viaje else None,
            }               
            request.session['viaje'] = json.dumps(viaje_data, cls=DjangoJSONEncoder)
            
            return redirect('../1/carga')
        else:
            print("formulario invalido..........")
            print(form.errors)
    else:
        form = Card1DestinatarioForm()
    print("---destinatario---zzzzzzz")     
    return render(request, 'card1destinatario.html', {'form': form})
    

def logistica_carga(request):
    print("---carga---")    
    
    remitente_info = request.session.get('remitente_info', None)
    destinatario_info = request.session.get('destinatario_json', None)
    viaje_ = request.session.get('viaje', '{}')       
    request.session['remitente_info'] = remitente_info
    request.session['destinatario_info'] = destinatario_info
    print("2---")                     
    """     
        return redirect('../1/pago')"""
    viaje = json.loads(viaje_)
    viaje_id = viaje.get('ID_Viaje')
        
    registros_de_carga = Carga.objects.filter(viaje__ID_Viaje=viaje_id)
    context = {
        'remitente_info': remitente_info,
        'destinatario_info': destinatario_info,
        'viaje': viaje,
        'registros_de_carga': registros_de_carga,
    }   
    return render(request, 'card1carga.html',context)

def agregar_carga(request):    
    if request.method == 'POST':
        
        form = CargaForm(request.POST)        
        
        if form.is_valid():
            carga = form.save(commit=False) 
            try:                
                carga.peso = Decimal(form.cleaned_data['peso'])                
            except decimal.InvalidOperation:
                return JsonResponse({'exito': False, 'errores': {'Peso': 'Por favor, ingrese un valor decimal válido.'}})

            carga_data = form.cleaned_data
            carga_data['nro_guia'] = str(uuid.uuid4())

            carga = Carga(**carga_data)
            carga.save()
            
            print(carga)
            
            viaje_json = request.session.get('viaje', '{}')
            viaje_data = json.loads(viaje_json)
            viaje_existente = Viaje.objects.get(ID_Viaje=viaje_data.get('ID_Viaje'))
            
            viaje_existente.Cargas.add(carga)
            
            viaje_existente.save()
            
            carga_dict = model_to_dict(carga)
            return JsonResponse({'exito': True, 'carga':carga_dict})
        else:
            return JsonResponse({'exito': False, 'errores': form.errors})
    else:
        form = CargaForm()

    return render(request, 'card1carga.html', {'form': form})


def eliminar_carga(request, carga_id):
    carga = get_object_or_404(Carga, pk=carga_id)
    try:
        carga.delete()
        return JsonResponse({'success': True, 'message': 'Carga eliminada con éxito'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def consultar_viaje(request):
    if request.method == 'GET':
        # Obtiene el número de guía de la solicitud GET
        numero_guia = request.GET.get('numero_guia', None)

        # Realiza la consulta del viaje por número de guía
        try:
            viaje = Viaje.objects.get(pk=numero_guia)
            registros_de_carga = Carga.objects.filter(viaje__ID_Viaje=numero_guia)
            registros_de_carga_list = [{'ID_Carga': carga.ID_Carga, 'nro_guia': carga.nro_guia, 'tipo_carga': carga.tipo_carga, 'cantidad_carga': carga.cantidad_carga, 'fecha_salida': carga.fecha_salida, 'costo_flete': carga.costo_flete, 'asegurar_carga': carga.asegurar_carga} for carga in registros_de_carga]
            data = {
                'numero_guia': viaje.ID_Viaje,
                'guia_zarpe': viaje.Guía_zarpe,
                'motonave': str(viaje.Motonave),
                'piloto': str(viaje.Piloto),
                'Remitente': {
                    'fname': viaje.Remitente.fname,
                    'tipodocumento': viaje.Remitente.tipodocumento,
                    'adr': viaje.Remitente.adr,
                    'email': viaje.Remitente.email,
                    'dep': viaje.Remitente.dep,
                    'empresa': viaje.Remitente.empresa,
                    'apellidos': viaje.Remitente.apellidos,
                    'documento': viaje.Remitente.documento,
                    'telefono': viaje.Remitente.telefono,
                    'city': viaje.Remitente.city,
                },
                'Destinatario': {
                    'fname': viaje.Destinatario.fname,
                    'tipodocumento': viaje.Destinatario.tipodocumento,
                    'adr': viaje.Destinatario.adr,
                    'email': viaje.Destinatario.email,
                    'dep': viaje.Destinatario.dep,
                    'empresa': viaje.Destinatario.empresa,
                    'apellidos': viaje.Destinatario.apellidos,
                    'documento': viaje.Destinatario.documento,
                    'telefono': viaje.Destinatario.telefono,
                    'city': viaje.Destinatario.city,
                },
                'Fecha_inicio_viaje': viaje.Fecha_inicio_viaje.isoformat() if viaje.Fecha_inicio_viaje else None,
                'Fecha_fin_viaje': viaje.Fecha_fin_viaje.isoformat() if viaje.Fecha_fin_viaje else None,
                'registros_de_carga': registros_de_carga_list,
                # Agrega más campos según tus necesidades
            }
            return JsonResponse({'success': True, 'data': data})
        except Viaje.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Viaje no encontrado'})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

def logistica_pago(request):
    print("--pago---")   
    form_data = request.session.get('form_data')
    if form_data:
        first_name = form_data.get('fname')
        tipodocumento = form_data.get('tipodocumento')
        print(first_name)
        print(tipodocumento) 
    if request.method == 'POST':
        request.session['form_data'] = request.POST
        return redirect('../1/revision')
    return render(request, 'card1pago.html')

def logistica_revision(request):
    print("---Revision---")  
    form_data = request.session.get('form_data')
    if form_data:
        first_name = form_data.get('firstname')
        tipodocumento = form_data.get('tipodocumento')
        print(first_name)
        print(tipodocumento)  
    return render(request, 'card1revision.html')


def informes(request):
    return render(request, 'card2.html')

def notificaciones(request):
    return render(request, 'card3.html')