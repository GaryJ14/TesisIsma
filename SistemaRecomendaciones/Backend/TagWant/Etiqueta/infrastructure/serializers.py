# Infraestructura: serializers/etiqueta_serializer.py
from rest_framework import serializers
from Backend.TagWant.Etiqueta.infrastructure.models import Etiqueta as EtiquetaModel

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtiquetaModel
        fields = ['id', 'nombre']
