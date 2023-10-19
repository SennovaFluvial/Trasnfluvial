from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home2'),
    path('', views.index, name='index'),
    path('card/1', views.logistica, name='LOGÍSTICA'),
    path('card/2', views.informes, name='INFORMES'),
    path('card/3', views.notificaciones, name='NOTIFICACIONES'),
]