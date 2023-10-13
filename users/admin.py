from django.contrib import admin

# Register your models here.
from .models import Roll, RollUser, Menu, Dependencia, DetalleUser, Solicitud


admin.site.register(Roll)
admin.site.register(RollUser)
admin.site.register(Menu)
admin.site.register(Dependencia)
admin.site.register(Solicitud)
admin.site.register(DetalleUser)