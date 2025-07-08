from django.db import models
from Backend.WantMusic.Contenido.infrastructure.models import Contenido
from Backend.TagWant.Etiqueta.infrastructure.models import Etiqueta

class ContenidoEtiqueta(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='relaciones_etiquetas')
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE, related_name='relaciones_contenido')

    class Meta:
        unique_together = ('contenido', 'etiqueta')
