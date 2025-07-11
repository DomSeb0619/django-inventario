from django.db import models

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Articulo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    observacion = models.TextField()
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    ubicacion_actual = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes_articulos/')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class HistorialMovimiento(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    ubicacion_origen = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, related_name='origen')
    ubicacion_destino = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, related_name='destino')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Movimiento de {self.articulo.codigo} el {self.fecha.strftime("%Y-%m-%d %H:%M:%S")}'


