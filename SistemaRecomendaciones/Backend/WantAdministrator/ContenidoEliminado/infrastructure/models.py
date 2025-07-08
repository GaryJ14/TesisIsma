from django.db import models
from Backend.WantMusic.Contenido.infrastructure.models import Contenido
from Backend.WantMusic.Usuario.infrastructure.models import Usuario
class ContenidoEliminado(models.Model):
    contenido = models.ForeignKey(    Contenido,    on_delete=models.CASCADE,    null=True)
    fecha_eliminacion = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True, null=True)
    eliminado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Eliminado: contenido_id={self.contenido_id} en {self.fecha_eliminacion.strftime('%Y-%m-%d %H:%M')}"
