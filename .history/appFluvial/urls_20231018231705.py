from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home2'),
    path('', views.index, name='index'),
    path('card/1', views.logistica, name='LOGÍSTICA-REMITENTE'),
    path('card/1/remitente', views.logistica, name='LOGÍSTICA-REMITENTE'),
    path('card/1/carga', views.logistica_carga, name='LOGÍSTICA-CARGA'),
    path('card/1/pago', views.logistica_pago, name='LOGÍSTICA-PAGO'),
    path('card/1/revision', views.logistica_revision, name='LOGÍSTICA-REVISIÓN'),
    path('card/2', views.informes, name='INFORMES'),
    path('card/3', views.notificaciones, name='NOTIFICACIONES'),
]