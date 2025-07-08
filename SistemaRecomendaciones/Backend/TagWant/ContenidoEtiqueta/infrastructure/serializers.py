from rest_framework import serializers
from Backend.TagWant.ContenidoEtiqueta.infrastructure.models import ContenidoEtiqueta

class ContenidoEtiquetaSerializer(serializers.Serializer):
    class Meta:
        model=ContenidoEtiqueta
        fields=['contenido_id','etiqueta_id']