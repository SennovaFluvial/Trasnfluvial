from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/login/', views.login_view, name='login'),
    
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LoginView.as_view(), name='logout'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    #path('accounts/login/signup/', views.signup, name='signup'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('consultar_viaje/', views.consultar_viaje, name='consultar_viaje'),
    path('card/1', login_required(views.logistica), name='LOGÍSTICA-REMITENTE'),
    #path('card/1', views.logistica, name='LOGÍSTICA-REMITENTE'),
    path('obtener-municipios/', views.obtener_municipios, name='obtener_municipios'),
    path('obtener_destinatario_por_cedula/', views.obtener_destinatario_por_cedula, name='obtener_destinatario_por_cedula'),
    path('agregar_carga/', views.agregar_carga, name='agregar_carga'),
    path('obtener_info_carga/<int:carga_id>/', views.obtener_info_carga, name='obtener_info_carga'),
    path('eliminar_carga/<int:carga_id>/', views.eliminar_carga, name='eliminar_carga'),
    path('card/1/remitente', views.logistica, name='LOGÍSTICA-REMITENTE'),
    path('card/1/destinatario', views.logistica_destinatario, name='LOGÍSTICA-DESTINATARIO'),
    path('card/1/carga', views.logistica_carga, name='LOGÍSTICA-CARGA'),
    path('card/1/pago', views.logistica_pago, name='LOGÍSTICA-PAGO'),
    path('card/1/revision', views.logistica_revision, name='LOGÍSTICA-REVISIÓN'),
    path('card/2', login_required(views.informes), name='INFORMES'),
    path('card/2/rep1', login_required(views.informe1), name='INFORME1'),
    path('card/2/rep2', login_required(views.informe2), name='INFORME2'),
    path('card/2/rep3', login_required(views.informe3), name='INFORME3'),
    path('card/2/rep4', login_required(views.informe4), name='INFORME4'),
    path('card/3', login_required(views.notificaciones), name='NOTIFICACIONES'),
]