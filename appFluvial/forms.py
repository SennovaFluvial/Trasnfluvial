# forms.py

from django import forms
from .models import Carga, Departamento, Destinatario, Pago
from .models import Municipio
from django.contrib.auth.forms import AuthenticationForm

class MiAuthenticationForm(AuthenticationForm):
    # Puedes personalizar el formulario si es necesario
    pass


    

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
    

class Card1DestinatarioForm(forms.ModelForm):    
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
        model = Destinatario  # 
        fields = '__all__'  
    

class CargaForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = '__all__'
        
        
""" 

class TuFormularioDePago(forms.ModelForm):
    tipo_pago = forms.ChoiceField(choices=[('pago en efectivo', 'pago en efectivo'),('pago por transferencia', 'pago por transferencia'),], label='Tipo Pago: ', required=True)
    valor_pagado = forms.CharField(label='Valor pagado: ', initial=total_cargas_viaje, max_length=20, required=True)
    titular_cuenta= forms.CharField(label='Titular de la cuenta: ', max_length=20, required=True)
    numero_cuenta= forms.CharField(label='Numero de cuenta: ', max_length=20, required=True)
    fecha_transaccion= forms.CharField(label='Fecha de la transaccion: ', max_length=20, required=True)
    
    def __init__(self, *args, **kwargs):
        super(TuFormularioDePago, self).__init__(*args, **kwargs)
        
        # Setear el valor predeterminado y hacer el campo ineditable
        self.fields['valor_pagado'].widget.attrs['readonly'] = True
        self.fields['valor_pagado'].widget.attrs['class'] = 'mi-clase-estilo'
        #self.fields['valor_pagado'].initial = '0.00'  
    def setvalue(self, arg):
        self.valor_pagado = arg
          
    class Meta:
        model = Pago
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super().clean()
        tipo_pago = cleaned_data.get('tipo_pago')
        titular_cuenta = cleaned_data.get('titular_cuenta')
        numero_cuenta = cleaned_data.get('numero_cuenta')
        fecha_transaccion = cleaned_data.get('fecha_transaccion')

        if tipo_pago == 'transferencia':
            if not titular_cuenta:
                raise forms.ValidationError("El valor pagado es obligatorio para tipo de pago transferencia.")
            if not numero_cuenta:
                raise forms.ValidationError("El Numero de cuenta es obligatorio para tipo de pago transferencia.")
            if not fecha_transaccion:
                raise forms.ValidationError("La Fecha de transación es obligatoria para tipo de pago transferencia.")

    
            # Validaciones específicas para efectivo
            # Puedes agregar más validaciones según sea necesario para efectivo

        # Agrega otras validaciones según tus necesidades
        
"""