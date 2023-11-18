import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import CardDescription, Destinatario

from .forms import Card1RemitenteForm
from .models import Departamento, Municipio
from django.contrib import messages

# def home(request):
#    return render(request, 'home.html')

def index(request):
    cards = CardDescription.objects.all()
    return render(request, 'index.html', {'cards': cards})


from django.shortcuts import get_object_or_404

def logistica(request):
    print("---remitente---")     
    #municipios = Municipio.objects.none()  
    #departamentos = Departamento.objects.all()

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
            else:
                # Si no existe, guardar como un nuevo registro
                # Si no existe, guardar como un nuevo registro
                new_destinatario = form.save()
                messages.success(request, 'Destinatario agregado exitosamente.')

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
    # Obtener la información del destinatario desde la sesión
    remitente_json = request.session.get('remitente_info', None)

    if remitente_json:
        # Deserializar el JSON para obtener el objeto del destinatario
        remitente_info = json.loads(remitente_json)
        # Ahora puedes usar destinatario_info como un diccionario que contiene la información del destinatario
        # ...
        print(remitente_info)
    form_data = request.session.get('form_data')
    if form_data:
        first_name = form_data.get('fname')
        tipodocumento = form_data.get('tipodocumento')
        apellidos = form_data.get('apellidos')
        print(" Nombres: ",first_name)
        print(" tipo documento: ",tipodocumento)
        print(" apellidos: " , apellidos)           
    if request.method == 'POST':
        request.session['form_data'] = request.POST
        return redirect('../1/carga')
    return render(request, 'card1destinatario.html')


def logistica_carga(request):
    print("---carga---")
    form_data = request.session.get('form_data')
    if form_data:
        first_name = form_data.get('fname')
        tipodocumento = form_data.get('tipodocumento')
        apellidos = form_data.get('apellidos')
        print(" Nombres: ",first_name)
        print(" tipo documento: ",tipodocumento)
        print(" apellidos: " , apellidos)           
    if request.method == 'POST':
        request.session['form_data'] = request.POST
        return redirect('../1/pago')
    return render(request, 'card1carga.html')

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