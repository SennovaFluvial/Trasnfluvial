# forms.py

from django import forms
from .models import Departamento, Destinatario
from .models import Municipio

class Card1RemitenteForm(forms.ModelForm):    
    fname = forms.CharField(label='Nombres Remitente', max_length=100, required=True)
    tipodocumento = forms.ChoiceField(choices=[('CC', 'CC'), ('CE', 'CE'), ('Pasaporte', 'Pasaporte')], label='Tipo documento', required=True)
    adr = forms.CharField(label='Dirección', max_length=255, required=True)
    email = forms.EmailField(label='Email', required=True)
    apellidos = forms.CharField(label='Apellidos Remitente', max_length=100, required=True)
    documento = forms.CharField(label='Documento', max_length=20, required=True)
    telefono = forms.CharField(label='Teléfono', max_length=20, required=True)
    empresa = forms.CharField(label='Empresa', max_length=255, required=False)
    DEPARTAMENTO_CHOICES = [(departamento.id, departamento.nombre) for departamento in Departamento.objects.all()]
    dep = forms.ChoiceField(choices=[('', 'Seleccione...')] + DEPARTAMENTO_CHOICES, widget=forms.Select(attrs={'class': 'custom-select'}), required=True)
    CITY_CHOICES  = [(municipio.id, municipio.nombre) for municipio in Municipio.objects.all()]
    city = forms.ChoiceField(choices=[('', 'Seleccione...')] + CITY_CHOICES, widget=forms.Select(attrs={'class': 'custom-select'}), required=True)
    class Meta:
        model = Destinatario  # Asocia el formulario con tu modelo
        fields = '__all__'  
    

