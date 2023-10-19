from django.shortcuts import render, redirect
from .models import CardDescription

#def home(request):
#    return render(request, 'home.html')

def index(request):
    cards = CardDescription.objects.all()
    return render(request, 'index.html', {'cards': cards})

def logistica(request):
    print("------")
    if request.method == 'POST':
        request.session['form_data'] = request.POST
        return redirect('../carga')
    return render(request, 'card1.html')

def form_view(request):
    if request.method == 'POST':
        request.session['form_data'] = request.POST
        return redirect('../carga')
    return render(request, 'card1carga.html')

def carga_view(request):
    form_data = request.session.get('form_data')
    if form_data:
        first_name = form_data.get('firstname')
        # Accede a otros campos de formulario de la misma manera
        # ...
        # Limpia los datos de la sesión después de usarlos si es necesario
        #del request.session['form_data']
    return render(request, 'card1pago.html', {'first_name': first_name})


def logistica_carga(request):
    return render(request, 'card1carga.html')
def logistica_pago(request):
    return render(request, 'card1pago.html')
def logistica_revision(request):
    return render(request, 'card1revision.html')


def informes(request):
    return render(request, 'card2.html')

def notificaciones(request):
    return render(request, 'card3.html')