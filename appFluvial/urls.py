from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
urlpatterns = [
    #path('', views.home, name='home2'),
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', views.MiLoginView.as_view(), name='login'),
    path('consultar_viaje/', views.consultar_viaje, name='consultar_viaje'),
    #path('card/1', login_required(views.logistica), name='LOGÍSTICA-REMITENTE'),
    path('card/1', views.logistica, name='LOGÍSTICA-REMITENTE'),
    path('obtener-municipios/', views.obtener_municipios, name='obtener_municipios'),
    path('obtener_destinatario_por_cedula/', views.obtener_destinatario_por_cedula, name='obtener_destinatario_por_cedula'),
    path('agregar_carga/', views.agregar_carga, name='agregar_carga'),
    path('eliminar_carga/<int:carga_id>/', views.eliminar_carga, name='eliminar_carga'),
    path('card/1/remitente', views.logistica, name='LOGÍSTICA-REMITENTE'),
    path('card/1/destinatario', views.logistica_destinatario, name='LOGÍSTICA-DESTINATARIO'),
    path('card/1/carga', views.logistica_carga, name='LOGÍSTICA-CARGA'),
    path('card/1/pago', views.logistica_pago, name='LOGÍSTICA-PAGO'),
    path('card/1/revision', views.logistica_revision, name='LOGÍSTICA-REVISIÓN'),
    path('card/2', views.informes, name='INFORMES'),
    path('card/3', views.notificaciones, name='NOTIFICACIONES'),
]