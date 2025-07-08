from django.db import models

class EstadisticaUsuario(models.Model):
    total_usuarios = models.IntegerField()
    total_activos = models.IntegerField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Usuarios totales: {self.total_usuarios} (Activos: {self.total_activos})"
