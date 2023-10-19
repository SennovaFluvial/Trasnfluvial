from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home2'),
    path('', views.index, name='index'),
    path('', views.card1, name='LOGÍSTICA'),
]