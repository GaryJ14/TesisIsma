from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from Backend.WantMusic.Contenido.infrastructure.repositories.contenido_adapter import ContenidoAdapter
from Backend.WantMusic.HistorialReproduccion.infrastructure.repositories.historialRep_adapter import HistorialReproduccionAdapter
from Backend.WantMusic.HistorialReproduccion.applications.service.historialRep_service import HistorialReproduccionService
from Backend.WantMusic.Contenido.infrastructure.serializers import ContenidoSerializer
from Backend.TagWant.ContenidoEtiqueta.infrastructure.repositories.contenidoEti_adapter import ContenidoEtiquetaAdapter
from Backend.WantMusic.Usuario.infrastructure.repositories.usuario_adapter import UsuarioAdapter  
# Instancia global opcional
servicio = HistorialReproduccionService(
    historial_repo=HistorialReproduccionAdapter(),
    contenido_repo=ContenidoAdapter(),
    relacion_repo=ContenidoEtiquetaAdapter(),
    usuario_repo=UsuarioAdapter()  
)

class HistorialReproduccionView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.servicio = HistorialReproduccionService(
            historial_repo=HistorialReproduccionAdapter(),
            contenido_repo=ContenidoAdapter(),
            relacion_repo=ContenidoEtiquetaAdapter(),
            usuario_repo=UsuarioAdapter()  
        )

    def get(self, request):
        historial = self.servicio.obtener_historial_detallado(request.user.id)
        serializer = ContenidoSerializer(historial, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        usuario_id = request.user.id
        contenido_id = request.data.get('contenido_id')
        duracion_visto = request.data.get('duracion_visto', None)

        if not contenido_id:
            return Response({"error": "contenido_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.servicio.agregar_historial(usuario_id, contenido_id, duracion_visto)
            return Response({"mensaje": "Historial registrado"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EliminarHistorial(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, contenido_id):
        resultado = servicio.eliminar_historial(request.user.id, contenido_id)
        if resultado:
            return Response({'mensaje': 'Contenido eliminado del historial'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Contenido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class EliminarTodoHistorial(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        servicio.eliminar_todo_historial(request.user.id)
        return Response({'mensaje': 'Todo el historial ha sido eliminado'}, status=status.HTTP_200_OK)
