# Backend/TagWant/infraestructura/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Backend.TagWant.Etiqueta.infrastructure.serializers import EtiquetaSerializer
from Backend.WantMusic.Contenido.infrastructure.serializers import ContenidoSerializer

from Backend.TagWant.Etiqueta.infrastructure.repositories.etiqueta_adapter import EtiquetaAdapter
from Backend.WantMusic.Contenido.infrastructure.repositories.contenido_adapter import ContenidoAdapter
from Backend.TagWant.ContenidoEtiqueta.infrastructure.repositories.contenidoEti_adapter import ContenidoEtiquetaAdapter

from Backend.TagWant.Etiqueta.applications.service.etiqueta_service import EtiquetaServicio


# Clase base para inyectar dependencias del servicio
class BaseEtiquetaView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        etiqueta_repo = EtiquetaAdapter()
        contenido_repo = ContenidoAdapter()
        relacion_repo = ContenidoEtiquetaAdapter()
        self.servicio = EtiquetaServicio(etiqueta_repo, contenido_repo, relacion_repo)


class ListaEtiquetasView(BaseEtiquetaView):
    def get(self, request):
        etiquetas = self.servicio.listar_todas()
        serializer = EtiquetaSerializer(etiquetas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ObtenerEtiquetaView(BaseEtiquetaView):
    def get(self, request, id):
        try:
            etiqueta = self.servicio.obtener_etiqueta_por_id(int(id))
            serializer = EtiquetaSerializer(etiqueta)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class CrearEtiquetaView(BaseEtiquetaView):
    def post(self, request):
        nombre = request.data.get('nombre')
        if not nombre:
            return Response({"error": "El campo 'nombre' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            etiqueta = self.servicio.crear_etiqueta(nombre)
            serializer = EtiquetaSerializer(etiqueta)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ActualizarEtiquetaView(BaseEtiquetaView):
    def put(self, request, id):
        nombre = request.data.get('nombre')
        if not nombre:
            return Response({"error": "El campo 'nombre' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            etiqueta = self.servicio.actualizar_etiqueta(int(id), nombre)
            serializer = EtiquetaSerializer(etiqueta)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class EliminarEtiquetaView(BaseEtiquetaView):
    def delete(self, request, id):
        try:
            self.servicio.eliminar_etiqueta(int(id))
            return Response({"mensaje": "Etiqueta eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


