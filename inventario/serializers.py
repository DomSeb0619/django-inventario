from rest_framework import serializers
from .models import Ubicacion, Articulo, HistorialMovimiento


class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'


class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = '__all__'


class HistorialMovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialMovimiento
        fields = '__all__'
