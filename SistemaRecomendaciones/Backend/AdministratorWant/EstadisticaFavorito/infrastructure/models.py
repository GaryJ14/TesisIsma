from django.db import models
from django.utils import timezone
class EstadisticaFavorito(models.Model):
    etiqueta = models.CharField(max_length=100, default="Mis Favoritos")    
    total_contenidos = models.IntegerField()
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Contenidos con etiqueta '{self.etiqueta}': {self.total_contenidos}"