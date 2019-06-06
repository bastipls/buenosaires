from django.contrib import admin
from .models import Usuario,Producto,Producto_proveedor,Orden,Solicitud

admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Producto_proveedor)
admin.site.register(Orden)
admin.site.register(Solicitud)

# Register your models here.
