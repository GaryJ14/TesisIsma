from django.db import models

class HistorialBusqueda(models.Model):
    usuario_id = models.IntegerField() 
    termino_busqueda = models.CharField(max_length=255)
    fecha_busqueda = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Búsqueda: {self.termino_busqueda} (usuario_id: {self.usuario_id})"
