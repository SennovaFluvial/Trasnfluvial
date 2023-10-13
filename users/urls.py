from django.urls import include
from django.contrib import admin
from django.urls import path

#from sariBack.views import hola_mundo,get_all_contacts,delete_all_contacts,get_data_from_google_sheet,get_data_from_google_sheetAll,delete_last_contact

from . import views

urlpatterns = [
    #path('home/', hola_mundo, name='hola_mundo'),
    path('', views.login),    
]

"""path('welcome', views.welcome),
    path('register', views.register),
    path('verificado', views.verificado),
    path('verificador/<str:token1>', views.verificado2),
    path('login', views.login),
    path('logout', views.logout),
    path('cambiarContraseña', views.cambiarContraseña),
    path('menu', views.menu),
    path('newsolicitud', views.newsolicitud),
    path('solicitudes', views.solicitudes),
    path('revisarSolic/<int:id_solicitud>', views.revisarSolic),
    path('corregirSolicitud/<int:id_solicitud>', views.corregirSolicitud),
    path('borrarSolicitud/<int:id_solicitud>', views.borrarSolicitud),
    path('bansolicitudes', views.bandejasolicitudes),
    path('historialSolicitudes', views.historialSolicitudes),
    path('reporteSolicitudes', views.reporteSolicitudes),
    path('enviarSolicitud', views.enviarSolicitud),
    path('revisarSolicitud/<str:home_>/<int:id_solicitud>', views.revisarSolicitud),
    path('verSolicitud/<int:id_solicitud>', views.verSolicitud),
    path('verSolicitudRep/<int:id_solicitud>', views.verSolicitudRep),
    path('revisarSolicitudRep/<int:id_solicitud>', views.revisarSolicitudRep),
    path('bandejaSolicitudes', views.bandejaSolicitudes),
    path('revisarSolicitudByTalento/<int:id_solicitud>', views.revisarSolicitudByTalento),
    path('solicitudesAprobadas', views.solicitudesAprobadas),
    path('verSolicitudAprobada/<int:id_solicitud>', views.verSolicitudAprobada),
    path('solicitudesVerificador', views.solicitudesVerificador),
    path('versolicitudVerificada/<int:id_solicitud>', views.versolicitudVerificada),
    path('solicitudesVerificadas', views.solicitudesVerificadas),
    path('registrarUsuario', views.registrarUsuario),
    path('usuariosRegistrados', views.usuariosRegistrados),
    path('verDatosUsuario/<int:id_usuario>', views.verDatosUsuario),
    """