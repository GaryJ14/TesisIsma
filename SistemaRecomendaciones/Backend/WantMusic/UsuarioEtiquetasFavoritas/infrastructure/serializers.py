from rest_framework import serializers
from UsuarioEtiquetasFavoritas.infrastructure.models import UsuarioEtiquetaFavorita

class UsuarioEtiquetaFavoritaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioEtiquetaFavorita
        fields = ['usuario_id', 'etiqueta_id']
