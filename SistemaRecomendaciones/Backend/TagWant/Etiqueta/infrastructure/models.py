from django.db import models

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
