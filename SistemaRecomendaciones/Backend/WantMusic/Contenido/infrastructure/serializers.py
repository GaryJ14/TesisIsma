from rest_framework import serializers
from Backend.WantMusic.Contenido.infrastructure.models import Contenido
from Backend.TagWant.Etiqueta.domain.entities.etiqueta_model import Etiqueta

class ContenidoSerializer(serializers.ModelSerializer):
    etiquetas = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    
    archivo = serializers.SerializerMethodField(read_only=True)
    etiquetas_asociadas = serializers.SerializerMethodField(read_only=True)
    subido_por_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Contenido
        fields = [
            'id',
            'titulo',
            'tipo',
            'archivo',
            'fecha_subida',
            'subido_por_id',
            'subido_por_nombre',
            'artista',
            'eliminado',
            'etiquetas',
            'etiquetas_asociadas'
        ]
        read_only_fields = [
            'id',
            'fecha_subida',
            'subido_por_id',
            'subido_por_nombre',
            'etiquetas_asociadas'
        ]

    def get_archivo(self, obj):
        request = self.context.get('request')
        archivo = getattr(obj, 'archivo', None)
        if archivo:
            # Evita doble /media/
            archivo = str(archivo)
            if archivo.startswith('/media/'):
                archivo = archivo[7:]
            elif archivo.startswith('media/'):
                archivo = archivo[6:]

            return request.build_absolute_uri(f'/media/{archivo}') if request else f'/media/{archivo}'
        return None


    def get_etiquetas_asociadas(self, obj):
        try:
            if hasattr(obj, 'etiquetas'):
                # Si fue asignado manualmente como lista
                if isinstance(obj.etiquetas, list):
                    return [e.nombre for e in obj.etiquetas]
                # Si viene de una relación ManyToMany
                return [e.nombre for e in obj.etiquetas.all()]
        except Exception:
            pass
        return []

    def get_subido_por_nombre(self, obj):
        return getattr(obj, 'subido_por_nombre', 'Anónimo')
