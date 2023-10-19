from django.shortcuts import render
from .models import CardDescription

#def home(request):
#    return render(request, 'home.html')

def index(request):
    cards = CardDescription.objects.all()
    return render(request, 'index.html', {'cards': cards})

def logistica(request):
    return render(request, 'card1.html')

def informes(request):
    return render(request, 'card2.html')

def notificaciones(request):
    return render(request, 'card3.html')