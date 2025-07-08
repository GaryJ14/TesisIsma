from rest_framework import serializers
from Backend.AdministratorWant.EstadisticaUsuario.infrastructure.models import EstadisticaUsuario

class EstadisticaUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadisticaUsuario
        fields = '__all__'
