from django.shortcuts import render, redirect
from .models import Ubicacion, Articulo
from django.core.files.storage import FileSystemStorage
from django.utils.dateparse import parse_date
from django.shortcuts import render

def ingresar_articulo(request):
    ubicaciones = Ubicacion.objects.all()
    if request.method == 'POST':
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        observacion = request.POST['observacion']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        ubicacion_id = request.POST['ubicacion']
        imagen = request.FILES['imagen']

        ubicacion = Ubicacion.objects.get(id=ubicacion_id)
        Articulo.objects.create(
            codigo=codigo,
            nombre=nombre,
            observacion=observacion,
            cantidad=cantidad,
            precio=precio,
            ubicacion_actual=ubicacion,
            imagen=imagen
        )
        return redirect('ingresar_articulo')

    return render(request, 'inventario/ingresar_articulo.html', {'ubicaciones': ubicaciones})

from .models import Articulo

def consultar_inventario(request):
    articulos = Articulo.objects.all()
    return render(request, 'inventario/consultar_inventario.html', {'articulos': articulos})

from .models import HistorialMovimiento

def historial_movimientos(request):
    movimientos = HistorialMovimiento.objects.select_related('articulo', 'ubicacion_origen', 'ubicacion_destino')
    return render(request, 'inventario/historial_movimientos.html', {'movimientos': movimientos})

from .models import Ubicacion

def registrar_ubicacion(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        if nombre.strip():
            Ubicacion.objects.create(nombre=nombre.strip())
        return redirect('registrar_ubicacion')
    
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'inventario/registrar_ubicacion.html', {'ubicaciones': ubicaciones})

from django.http import JsonResponse
from .models import Ubicacion, Articulo, HistorialMovimiento

def mover_inventario(request):
    articulos = Articulo.objects.select_related('ubicacion_actual')
    ubicaciones = Ubicacion.objects.all()

    # --- Ajax: devolver ubicación actual de un artículo ----------------------
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        art_id = request.GET.get('articulo_id')
        articulo = Articulo.objects.filter(id=art_id).select_related('ubicacion_actual').first()
        if articulo:
            return JsonResponse({'ubicacion': articulo.ubicacion_actual.nombre})
        return JsonResponse({}, status=404)
    # ------------------------------------------------------------------------

    if request.method == 'POST':
        art_id       = request.POST['articulo']
        nueva_ubi_id = request.POST['nueva_ubicacion']

        articulo        = Articulo.objects.get(id=art_id)
        ubicacion_origen = articulo.ubicacion_actual
        ubicacion_dest   = Ubicacion.objects.get(id=nueva_ubi_id)

        # Registrar movimiento
        HistorialMovimiento.objects.create(
            articulo=articulo,
            ubicacion_origen=ubicacion_origen,
            ubicacion_destino=ubicacion_dest
        )

        # Actualizar ubicación del artículo
        articulo.ubicacion_actual = ubicacion_dest
        articulo.save()

        return redirect('mover_inventario')

    context = {'articulos': articulos, 'ubicaciones': ubicaciones}
    return render(request, 'inventario/mover_inventario.html', context)

def dashboard(request):
    return render(request, 'inventario/dashboard.html')

def consultar_inventario(request):
    filtro = request.GET.get('filtro', '')
    ubicacion_id = request.GET.get('ubicacion')

    articulos = Articulo.objects.all()

    if filtro:
        articulos = articulos.filter(nombre__icontains=filtro) | articulos.filter(codigo__icontains=filtro)
    if ubicacion_id:
        articulos = articulos.filter(ubicacion_actual_id=ubicacion_id)

    ubicaciones = Ubicacion.objects.all()
    return render(request, 'inventario/consultar_inventario.html', {
        'articulos': articulos,
        'ubicaciones': ubicaciones,
        'filtro': filtro,
        'ubicacion_id': ubicacion_id
    })
def historial_movimientos(request):
    movimientos = HistorialMovimiento.objects.select_related('articulo', 'ubicacion_origen', 'ubicacion_destino')
    
    # Parámetros de filtro
    articulo_q = request.GET.get('articulo', '')
    origen_id = request.GET.get('origen', '')
    destino_id = request.GET.get('destino', '')
    desde = request.GET.get('desde', '')
    hasta = request.GET.get('hasta', '')

    if articulo_q:
        movimientos = movimientos.filter(
            articulo__nombre__icontains=articulo_q
        ) | movimientos.filter(
            articulo__codigo__icontains=articulo_q
        )

    if origen_id:
        movimientos = movimientos.filter(ubicacion_origen_id=origen_id)

    if destino_id:
        movimientos = movimientos.filter(ubicacion_destino_id=destino_id)

    if desde:
        movimientos = movimientos.filter(fecha__date__gte=parse_date(desde))
    if hasta:
        movimientos = movimientos.filter(fecha__date__lte=parse_date(hasta))

    ubicaciones = Ubicacion.objects.all()

    return render(request, 'inventario/historial_movimientos.html', {
        'movimientos': movimientos,
        'ubicaciones': ubicaciones,
        'articulo_q': articulo_q,
        'origen_id': origen_id,
        'destino_id': destino_id,
        'desde': desde,
        'hasta': hasta
    })

def home_dashboard(request):
    return render(request, 'inventario/home.html')

def home_dashboard(request):
    cards = [
        {"title": "Ingresar Artículo", "icon": "fas fa-plus-square", "url": "/ingresar-articulo/"},
        {"title": "Movimiento Inventario", "icon": "fas fa-exchange-alt", "url": "/mover-inventario/"},
        {"title": "Consultar Inventario", "icon": "fas fa-boxes", "url": "/consultar-inventario/"},
        {"title": "Historial Movimientos", "icon": "fas fa-history", "url": "/historial-movimientos/"},
    ]
    return render(request, 'inventario/home.html', {"cards": cards})