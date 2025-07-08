#traduce datos para enviarlos o recibirlos
# Define los serializadores para exponer los datos por API REST en formato JSON. PARTE 5

from rest_framework import serializers
from Backend.WantAdministrator.ContenidoEliminado.infrastructure.models import ContenidoEliminado

class ContenidoEliminadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenidoEliminado
        fields = ['id', 'contenido_id', 'fecha_eliminacion', 'motivo', 'eliminado_por_id']
