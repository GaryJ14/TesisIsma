from rest_framework import serializers
from Backend.AdministratorWant.EstadisticaFavorito.infrastructure.models import EstadisticaFavorito

class EstadisticaFavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadisticaFavorito
        fields = '__all__'
