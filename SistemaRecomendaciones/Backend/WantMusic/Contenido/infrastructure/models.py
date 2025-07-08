from django.db import models
import datetime

def ruta_personalizada(instance, filename):
    hoy = datetime.date.today()
    subcarpeta = f"{hoy.year}/{hoy.month:02d}"
    return f"{instance.tipo}/{subcarpeta}/{filename}"

class Contenido(models.Model):
    TIPO_CHOICES = [
        ('audio', 'Audio'),
        ('video', 'Video'),
    ]

    titulo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    archivo = models.URLField(max_length=800, null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    subido_por_id = models.IntegerField(null=True, blank=True)

    artista = models.CharField(max_length=255, null=True, blank=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
