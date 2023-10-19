from django.shortcuts import render
from .models import CardDescription

#def home(request):
#    return render(request, 'home.html')

def index(request):
    cards = CardDescription.objects.all()
    return render(request, 'index.html', {'cards': cards})

def logistica(request):
    return render(request, 'card1.html')

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