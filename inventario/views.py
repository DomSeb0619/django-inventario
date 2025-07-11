from rest_framework import viewsets
from .models import Ubicacion, Articulo, HistorialMovimiento
from .serializers import UbicacionSerializer, ArticuloSerializer, HistorialMovimientoSerializer


class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer


class ArticuloViewSet(viewsets.ModelViewSet):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer


class HistorialMovimientoViewSet(viewsets.ModelViewSet):
    queryset = HistorialMovimiento.objects.all()
    serializer_class = HistorialMovimientoSerializer
