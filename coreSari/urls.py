from django.urls import include
from django.contrib import admin
from django.urls import path

#from sariBack.views import hola_mundo,get_all_contacts,delete_all_contacts,get_data_from_google_sheet,get_data_from_google_sheetAll,delete_last_contact


urlpatterns = [
    #path('home/', hola_mundo, name='hola_mundo'),
    path('app/', include('appFluvial.urls')),
    path('admin/', admin.site.urls),
    path('logout/',include('appFluvial.urls')),
    path('',include('appFluvial.urls')),
    
]
