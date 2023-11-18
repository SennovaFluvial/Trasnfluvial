from django.shortcuts import render, redirect
from .models import CardDescription

from .forms import SelectDepartamentoForm
from .models import Departamento, Municipio

#def home(request):
#    return render(request, 'home.html')

def index(request):
    cards = CardDescription.objects.all()
    return render(request, 'index.html', {'cards': cards})

def mi_vista(request):
    departamentos = Departamento.objects.all()
    
    if request.method == 'POST':
        form = SelectDepartamentoForm(request.POST)
        if form.is_valid():
            departamento_seleccionado = form.cleaned_data['nombre']
            municipios = Municipio.objects.filter(departamento__nombre=departamento_seleccionado)
    else:
        form = SelectDepartamentoForm()
        municipios = Municipio.objects.none()

    return render(request, 'mi_template.html', {'form': form, 'municipios': municipios, 'departamentos': departamentos})

def logistica(request):
    print("---remitente---")
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
        
        return redirect('../../card/1/destinatario')
    return render(request, 'card1.html')

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