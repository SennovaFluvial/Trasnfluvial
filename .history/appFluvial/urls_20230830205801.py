from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home2'),
    path('', views.index, name='index'),
]