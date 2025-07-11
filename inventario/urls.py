from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UbicacionViewSet, ArticuloViewSet, HistorialMovimientoViewSet
from .views_front import ingresar_articulo
from .views_front import consultar_inventario, historial_movimientos
from .views_front import registrar_ubicacion
from .views_front import mover_inventario
from .views_front import home_dashboard

router = DefaultRouter()
router.register(r'ubicaciones', UbicacionViewSet)
router.register(r'articulos', ArticuloViewSet)
router.register(r'movimientos', HistorialMovimientoViewSet)

urlpatterns = [
    path('', home_dashboard, name='home_dashboard'),
    path('ingresar-articulo/', ingresar_articulo, name='ingresar_articulo'),
    path('consultar-inventario/', consultar_inventario, name='consultar_inventario'),
    path('historial-movimientos/', historial_movimientos, name='historial_movimientos'),
    path('registrar-ubicacion/', registrar_ubicacion, name='registrar_ubicacion'),
    path('mover-inventario/', mover_inventario, name='mover_inventario'),
    path('', include(router.urls)),
]
