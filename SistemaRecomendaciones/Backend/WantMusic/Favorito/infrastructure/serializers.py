from rest_framework import serializers
from Backend.WantMusic.Favorito.domain.entities.favorito_model import Favorito

class FavoritoSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    contenido_id = serializers.IntegerField()
    fecha_favorito = serializers.DateTimeField()
