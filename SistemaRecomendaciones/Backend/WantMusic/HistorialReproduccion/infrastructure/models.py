from django.db import models

class HistorialReproduccion(models.Model):
    usuario_id = models.IntegerField()     # Solo se guarda el ID
    contenido_id = models.IntegerField()   # Solo se guarda el ID
    fecha_reproduccion = models.DateTimeField(auto_now_add=True)
    duracion_visto = models.PositiveIntegerField(null=True, blank=True)
