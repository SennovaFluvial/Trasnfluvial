from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import CardDescription

from .forms import Card1RemitenteForm
from .models import Departamento, Municipio

# def home(request):
#    return render(request, 'home.html')

def index(request):
    cards = CardDescription.objects.all()
    return render(request, 'index.html', {'cards': cards})


def logistica(request):
    print("---remitente---")     
    municipios = Municipio.objects.none()  
    departamentos = Departamento.objects.all()
    if request.method == 'POST':
        print("22222222222222222222")
        form = Card1RemitenteForm(request.POST)
        
        if form.is_valid():
            destinatario_instance = form.save()    
            print(destinatario_instance)     
            return redirect('../../card/1/destinatario')
        else:
            print("formulario invalido..........")
            print(form.errors)
    else:
        form = Card1RemitenteForm()
        
    
    return render(request, 'card1.html', {'form': form, 'municipios': municipios, 'departamentos': departamentos})


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
    
def logistica_destinatario(request):
    print("---destinatario---")
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