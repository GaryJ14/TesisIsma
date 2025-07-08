from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Backend.TagWant.ContenidoEtiqueta.infrastructure.repositories.contenidoEti_adapter import ContenidoEtiquetaAdapter
from Backend.TagWant.ContenidoEtiqueta.infrastructure.serializers import ContenidoEtiquetaSerializer
from Backend.TagWant.ContenidoEtiqueta.applications.service.contenidoEti_service import ContenidoEtiquetaServicio

class CrearContenidoEtiquetaView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.servicio = ContenidoEtiquetaServicio(ContenidoEtiquetaAdapter())

    def post(self, request):
        serializer = ContenidoEtiquetaSerializer(data=request.data)
        if serializer.is_valid():
            relacion = self.servicio.crear_relacion(
                serializer.validated_data['contenido_id'],
                serializer.validated_data['etiqueta_id']
            )
            return Response(ContenidoEtiquetaSerializer(relacion).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarContenidoEtiquetaView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.servicio = ContenidoEtiquetaServicio(ContenidoEtiquetaAdapter())

    def get(self, request):
        relaciones = self.servicio.listar()
        serializer = ContenidoEtiquetaSerializer(relaciones, many=True)
        return Response(serializer.data)

class EliminarContenidoEtiquetaView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.servicio = ContenidoEtiquetaServicio(ContenidoEtiquetaAdapter())

    def delete(self, request, id):
        self.servicio.eliminar(id)
        return Response({"mensaje": "Relación eliminada correctamente"}, status=status.HTTP_204_NO_CONTENT)
