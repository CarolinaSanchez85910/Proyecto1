from django.contrib import admin
from .models import Usuario, Establecimiento, Servicio, Reserva, Categoria

admin.site.register(Usuario)
admin.site.register(Establecimiento)
admin.site.register(Servicio)
admin.site.register(Reserva)
admin.site.register(Categoria)

