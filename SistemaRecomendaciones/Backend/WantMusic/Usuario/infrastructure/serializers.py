from rest_framework import serializers
from Backend.WantMusic.Usuario.infrastructure.models import Usuario 
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email','password', 'is_active', 'is_staff', 'creado_en', 'foto_perfil']
        read_only_fields = ['id', 'is_active', 'is_staff', 'creado_en']
        