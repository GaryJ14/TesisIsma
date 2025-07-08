from rest_framework import serializers
from Backend.WantMusic.HistorialReproduccion.infrastructure.models import HistorialReproduccion


class HistorialReproduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialReproduccion
        fields = ['id', 'usuario', 'contenido', 'fecha_reproduccion']