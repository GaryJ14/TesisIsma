from django.db import models

class UsuarioEtiquetaFavorita(models.Model):
    usuario_id = models.IntegerField()
    etiqueta_id = models.IntegerField()

    class Meta:
        unique_together = ('usuario_id', 'etiqueta_id')

    def __str__(self):
        return f"Usuario {self.usuario_id} - Etiqueta {self.etiqueta_id}"
