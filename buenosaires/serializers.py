from rest_framework import serializers
from .models import Producto_proveedor

class Producto_proveedorSerializador(serializers.ModelSerializer):
    class Meta:
        model = Producto_proveedor
        fields = '__all__'