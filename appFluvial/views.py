from decimal import Decimal
import decimal
from django import forms
from django.forms import model_to_dict
from django.utils import timezone
import json
import uuid
from django.http import JsonResponse
from django.shortcuts import render, redirect
from appFluvial.filters import DestinatarioFilter, ViajeFilter

from appFluvial.tables import TuModeloTableDestinatario,TuModeloTablePago,TuModeloTableCarga,TuModeloTableViaje
from .models import CardDescription, Carga, Destinatario, Pago, Parameter, Viaje

from .forms import Card1DestinatarioForm, Card1RemitenteForm, CargaForm, MiAuthenticationForm
from .models import Departamento, Municipio
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.serializers import serialize
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# def home(request):
#    return render(request, 'home.html')

def index(request):
    cards = CardDescription.objects.all()
    return render(request, 'index.html', {'cards': cards})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión después de registrarse
            return redirect('index')  # Redirige a la página principal después del registro
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

class MiLoginView(LoginView):
    template_name = 'appFluvial/login.html'
    form_class = MiAuthenticationForm
    success_url = reverse_lazy('logistica')

#@login_required
def logistica(request):
    print("---remitente---")     
    if request.method == 'POST':
        form = Card1RemitenteForm(request.POST)

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
        #remitente_info = json.loads(remitente_info)
        try:
            remitente_info = json.loads(remitente_info)
        except json.JSONDecodeError as e:
            return redirect('../card/1/remitente')
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
    try:
        viaje = json.loads(viaje_)
    except json.JSONDecodeError as e:
        return redirect('../card/1/remitente')
    viaje_id = viaje.get('ID_Viaje')
        
    registros_de_carga = Carga.objects.filter(viaje__ID_Viaje=viaje_id)
    context = {
        'remitente_info': remitente_info,
        'destinatario_info': destinatario_info,
        'viaje': viaje,
        'registros_de_carga': registros_de_carga,
    }  
    form = CargaForm() 
    print(form)
    return render(request, 'card1carga.html',context)

def agregar_carga(request):    
    if request.method == 'POST':        
        form = CargaForm(request.POST)        
                        
        if form.is_valid():
            carga = form.save(commit=False)                
            carga_data = form.cleaned_data
            print(carga_data)
            if carga_data['nro_guia'] is None or carga_data['nro_guia'] == '':
                carga_data['nro_guia'] = str(uuid.uuid4())

            carga_existente = Carga.objects.filter(nro_guia=carga_data['nro_guia']).first()
            existente = False
            if carga_existente:
                print("<existente>-------------------------------------------------------------")
                existente = True
                carga = carga_existente                
                for key, value in carga_data.items():
                    setattr(carga, key, value)
                
                par = Parameter.find_parameter_for_subtotal(carga.costo_flete) 
                #par = Parameter.objects.filter(key='factorSeguro').first()
                if not par: 
                    return JsonResponse({'exito': False, 'errores': 'No existe un parametro con el rango para factorSeguro'})
                
                factorSeguro = float(par.value)
                                
                if carga.asegurar_carga:
                    carga.total = float(carga.costo_flete) + float(carga.costo_flete)*factorSeguro
                    carga.factorSeguro = str(factorSeguro)
                else:
                    carga.total = carga.costo_flete
                    carga.factorSeguro = "0"
                
                carga.save()
            else:
                print("-------------------------------------------------------------<inexistente>")
                existente = False
                carga = Carga(**carga_data)
                
                par = Parameter.find_parameter_for_subtotal(carga.costo_flete) 
                #par = Parameter.objects.filter(key='factorSeguro').first()
                if not par: 
                    return JsonResponse({'exito': False, 'errores': 'No existe un parametro con el rango para factorSeguro'})
                
                
                factorSeguro = float(par.value)
                                
                if carga.asegurar_carga:
                    carga.total = float(carga.costo_flete) + float(carga.costo_flete)*factorSeguro
                    carga.factorSeguro = str(factorSeguro)
                else:
                    carga.total = carga.costo_flete
                    carga.factorSeguro = "0"
                
                carga.save()           
            
            viaje_json = request.session.get('viaje', '{}')
            
            try:
                viaje_data = json.loads(viaje_json)
            except json.JSONDecodeError as e:
                return redirect('../card/1/remitente')
            viaje_existente = Viaje.objects.get(ID_Viaje=viaje_data.get('ID_Viaje'))
            
            viaje_existente.Cargas.add(carga)
            
            viaje_existente.save()
            
            carga_dict = model_to_dict(carga)
            #return render(request, 'card1carga.html', {'form': form})
            
            return JsonResponse({'exito': True, 'carga':carga_dict,'existente':existente })
        else:
            print(form.errors)
            return JsonResponse({'exito': False, 'errores': form.errors})
    else:
        form = CargaForm()    
    return render(request, 'card1carga.html', {'form': form})

def obtener_info_carga(request, carga_id):
    carga = get_object_or_404(Carga, ID_Carga=carga_id)

    # Aquí, crea un diccionario con la información que deseas devolver
    carga_info = {
        'ID_Carga': carga.ID_Carga,
        'nro_guia': carga.nro_guia,
        'ciudad_carga': carga.ciudad_carga,
        'departamento_carga': carga.departamento_carga,
        'embarcacion': carga.embarcacion,
        'capitan': carga.capitan,
        'tipo_carga': carga.tipo_carga,
        'cantidad_carga': carga.cantidad_carga,
        'unidad_medida': carga.unidad_medida,
        'volumen_carga': carga.volumen_carga,
        'peso': carga.peso,
        'fecha_recibo': carga.fecha_recibo,
        'fecha_cargue': carga.fecha_cargue,
        'fecha_salida': carga.fecha_salida,
        'categoria': carga.categoria,
        'ruta': carga.ruta,
        'costo_flete': carga.costo_flete,
        'descripcion': carga.descripcion,
        'asegurar_carga': carga.asegurar_carga,
        'total':carga.total,
    }

    return JsonResponse({'carga': carga_info})

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

def validate_numero_cuenta(value):
    if not value:
        raise ValidationError(_('El número de cuenta no puede estar vacío.'), code='invalid')

def logistica_pago(request):
    print("--pago---")
    viaje_ = request.session.get('viaje', '{}') 
    try:
        viaje = json.loads(viaje_)
    except json.JSONDecodeError as e:
        return redirect('../card/1/remitente')
    
    viaje_id = viaje.get('ID_Viaje')
    #import pdb; pdb.set_trace()
    viaje_existente = Viaje.objects.get(pk=viaje_id)    
    
    if viaje_existente.Pagos is not None:
        pago = get_object_or_404(Pago, pk=viaje_existente.Pagos.pk)
        print(pago)
        if pago:         
            pago.delete()
        
    total_cargas_viaje = viaje_existente.calcular_total_cargas()
    #import pdb; pdb.set_trace()
    class TuFormularioDePago(forms.Form):
        tipo_pago = forms.ChoiceField(choices=[('pago en efectivo', 'pago en efectivo'),('pago por transferencia', 'pago por transferencia'),], label='Tipo Pago: ', required=True)
        valor_pagado = forms.CharField(label='Valor pagado', initial=total_cargas_viaje, max_length=20, required=True)
        titular_cuenta= forms.CharField(label='Titular de la cuenta', max_length=20, required=True)
        numero_cuenta= forms.CharField(label='Numero de cuenta', max_length=20, required=True, validators=[validate_numero_cuenta])
        fecha_transaccion= forms.DateField(label='Fecha de la transaccion',  required=True, widget=forms.DateInput(attrs={'type': 'date'}))
        
        def __init__(self, *args, **kwargs):
            super(TuFormularioDePago, self).__init__(*args, **kwargs)            
            self.fields['valor_pagado'].widget.attrs['readonly'] = True
            self.fields['valor_pagado'].widget.attrs['class'] = 'mi-clase-estilo'
            self.fields['valor_pagado'].widget.attrs['onchange'] = 'ocultarCampo();'
        def setvalue(self, arg):
            self.valor_pagado = arg
            
        class Meta:
            model = Pago
            fields = '__all__'
            
            def clean(self):
                cleaned_data = super().clean()
                tipo_pago = cleaned_data.get('tipo_pago')

                if tipo_pago == 'pago por transferencia':
                    if not cleaned_data.get('numero_cuenta'):
                        raise ValidationError({'numero_cuenta': _('El número de cuenta es obligatorio.')})

            def save(self, *args, **kwargs):
                self.clean()
                super().save(*args, **kwargs)
    
    pago_form = TuFormularioDePago(request.POST)    
    if request.method == 'POST':      
        print(total_cargas_viaje)
        
        if pago_form.is_valid():
            pago_data = pago_form.cleaned_data
            pago = Pago(**pago_data)
            pago.save()
            
            viaje_existente.Pagos=pago                        
            viaje_existente.save()
            #import pdb; pdb.set_trace()
            pago_serializado = serialize('json', [pago])
            request.session['pago'] = pago_serializado          
            return redirect('../1/revision')
        else:
            for field, errors in pago_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            print("El formulario no es válido. Manejar de alguna manera.")

            print(pago_form.errors)

    else:
        pago_form = TuFormularioDePago()
    return render(request, 'card1pago.html', {'pago_form': pago_form, 'total_cargas_viaje':total_cargas_viaje})



def logistica_revision(request):
    print("---Revision---")  
    viaje_ = request.session.get('viaje', '{}') 
    try:
        viaje = json.loads(viaje_)
    except json.JSONDecodeError as e:
        return redirect('../../card/1/remitente')
    viaje_id = viaje.get('ID_Viaje')
    viaje_existente = Viaje.objects.get(pk=viaje_id) 
    
    remitente_info_ = request.session.get('remitente_info', None)
    remitente_info = json.loads(remitente_info_) if isinstance(remitente_info_, str) else remitente_info_

    destinatario_info_ = request.session.get('destinatario_json', None)
    destinatario_info = json.loads(destinatario_info_) if isinstance(destinatario_info_, str) else destinatario_info_

    pago_info_ = request.session.get('pago', None)
    pago_info = json.loads(pago_info_) if isinstance(pago_info_, str) else pago_info_


    
    registros_de_carga = Carga.objects.filter(viaje__ID_Viaje=viaje_id)
    #registros = serialize('json', [registros_de_carga])
    context = {
        'remitente': remitente_info,
        'destinatario': destinatario_info,
        'viaje': viaje,
        'cargas': registros_de_carga,
        'pago':pago_info
    } 
    
    print(viaje)
    print("__________________________________registros_de_carga")
    print(registros_de_carga)
    print("__________________________________pago_info")
    print(pago_info)
    print("__________________________________")
    if request.POST:
        request.session['remitente_info'] = ""
        request.session['destinatario_json'] = ""
        request.session['destinatario_info'] = ""
        request.session['viaje'] = ""
        request.session['pago'] = ""     
        return redirect('../../card/1/remitente')
    return render(request, 'card1revision.html',context)


def informes(request):
    return render(request, 'card2.html')

def informe1(request):
    data = Viaje.objects.all()
    filter = ViajeFilter(request.GET, queryset=data)
    table = TuModeloTableViaje(filter.qs)
    return render(request, 'card2inf1.html', {'table': table, 'filter': filter})


def informe2(request):
    data = Destinatario.objects.all()
    filter = DestinatarioFilter(request.GET, queryset=data)
    table = TuModeloTableDestinatario(filter.qs)
    return render(request, 'card2inf2.html',  {'table': table, 'filter': filter})

def informe3(request):
    data = Carga.objects.all()
    table = TuModeloTableCarga(data)
    return render(request, 'card2inf3.html',  {'table': table})

def informe4(request):
    data = Pago.objects.all()
    table = TuModeloTablePago(data)
    return render(request, 'card2inf4.html',  {'table': table})

def notificaciones(request):
    return render(request, 'card3.html')