from rest_framework import serializers
from Backend.WantMusic.HistorialBusqueda.infrastructure.models import HistorialBusqueda

class HistorialBusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialBusqueda
        fields = ['id', 'usuario_id', 'termino_busqueda', 'fecha_busqueda']
