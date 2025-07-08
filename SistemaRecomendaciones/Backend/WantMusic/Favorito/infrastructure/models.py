from django.db import models

class Favorito(models.Model):
    usuario_id = models.IntegerField()     # solo ID
    contenido_id = models.IntegerField()   # solo ID
    fecha_favorito = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario_id', 'contenido_id')
