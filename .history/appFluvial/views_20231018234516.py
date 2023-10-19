from django.shortcuts import render, redirect
from .models import CardDescription

#def home(request):
#    return render(request, 'home.html')

def index(request):
    cards = CardDescription.objects.all()
    return render(request, 'index.html', {'cards': cards})

def logistica(request):
    print("---remitente---")
    form_data = request.session.get('form_data')
    if form_data:
        first_name = form_data.get('firstname')
        tipodocumento = form_data.get('tipodocumento')
        print(first_name)
        print(tipodocumento)
    if request.method == 'POST':
        request.session['form_data'] = request.POST
        return redirect('../1/carga')
    return render(request, 'card1.html')

########################################################
def otracosa_view(request):
    form_data = request.session.get('form_data')
    if form_data:
        first_name = form_data.get('firstname')
        
    return render(request, 'card1pago.html', {'first_name': first_name})
#########################################################

def logistica_carga(request):
    print("---carga---")
    form_data = request.session.get('form_data')
    if form_data:
        first_name = form_data.get('firstname')
        tipodocumento = form_data.get('tipodocumento')
        print(first_name)
        print(tipodocumento)            
    if request.method == 'POST':
        request.session['form_data'] = request.POST
        return redirect('../1/pago')
    return render(request, 'card1carga.html')

def logistica_pago(request):
    print("--pago---")   
    form_data = request.session.get('form_data')
    if form_data:
        first_name = form_data.get('firstname')
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