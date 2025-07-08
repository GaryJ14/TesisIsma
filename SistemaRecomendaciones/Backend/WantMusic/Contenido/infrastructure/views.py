import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser  
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from Backend.WantMusic.Contenido.applications.service.contenido_service import ContenidoServicio
from Backend.WantMusic.Contenido.infrastructure.serializers import ContenidoSerializer
from Backend.WantMusic.Contenido.infrastructure.repositories.contenido_adapter import ContenidoAdapter
from Backend.TagWant.Etiqueta.infrastructure.repositories.etiqueta_adapter import EtiquetaAdapter
from Backend.TagWant.ContenidoEtiqueta.infrastructure.repositories.contenidoEti_adapter import ContenidoEtiquetaAdapter
from Backend.WantAdministrator.ContenidoEliminado.infrastructure.repositories.contenidoElim_adapter import ContenidoEliminadoAdapter
from Backend.WantMusic.Usuario.infrastructure.repositories.usuario_adapter import UsuarioAdapter
from Backend.WantMusic.UsuarioEtiquetasFavoritas.infrastructure.repositories.usuarioEtiFav_adapter import UsuarioEtiquetaFavoritaAdapter


class BaseContenidoView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.servicio = ContenidoServicio(
            contenido_repo=ContenidoAdapter(),
            etiqueta_repo=EtiquetaAdapter(),
            repositorio_relacion=ContenidoEtiquetaAdapter(),
            contenido_eliminado_repo=ContenidoEliminadoAdapter(),
            usuario_etiqueta_repo=UsuarioEtiquetaFavoritaAdapter(),
            usuario_repo=UsuarioAdapter()
        )


class CrearContenidoView(BaseContenidoView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContenidoSerializer(data=request.data)
        if serializer.is_valid():
            datos = serializer.validated_data
            datos['subido_por_id'] = request.user
            archivo = request.FILES.get('archivo')
            contenido = self.servicio.crear_contenido_con_etiquetas(datos, archivo)
            return Response(ContenidoSerializer(contenido, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = ContenidoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                datos = serializer.validated_data
                datos['subido_por_id'] = request.user
                archivo = request.FILES.get('archivo')
                contenido = self.servicio.crear_contenido_con_etiquetas(datos, archivo)
                return Response(ContenidoSerializer(contenido, context={'request': request}).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print("❌ ERROR AL CREAR CONTENIDO:", e)
                traceback.print_exc()
                return Response({"error": str(e)}, status=500)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarContenidoView(BaseContenidoView):
    def get(self, request):
        contenidos = self.servicio.listar_contenidos()
        serializer = ContenidoSerializer(contenidos, many=True, context={'request': request})
        return Response(serializer.data)


class ActualizarContenidoView(BaseContenidoView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, pk):
        contenido = self.servicio.obtener_contenido(pk)
        if not contenido:
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContenidoSerializer(data=request.data)
        if serializer.is_valid():
            archivo = request.FILES.get("archivo")
            actualizado = self.servicio.actualizar_contenido(contenido, serializer.validated_data, archivo)
            return Response(ContenidoSerializer(actualizado, context={'request': request}).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EliminarContenidoView(BaseContenidoView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request, pk):
        motivo = request.data.get("motivo")
        if not motivo or not motivo.strip():
            return Response({"error": "Se debe proporcionar un motivo para la eliminación"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            eliminado = self.servicio.eliminar_contenido(pk, request.user, motivo)
            if eliminado:
                return Response({"mensaje": "Eliminado correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "No se pudo eliminar"}, status=status.HTTP_400_BAD_REQUEST)


class ContenidosPorEtiquetasFavoritasView(BaseContenidoView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario_id = request.user.id
        etiquetas_ids = self.servicio.obtener_etiquetas_favoritas(usuario_id)

        if not etiquetas_ids:
            return Response({"mensaje": "No tienes etiquetas favoritas registradas."}, status=200)

        contenidos_filtrados = self.servicio.listar_contenidos_por_etiquetas(etiquetas_ids)
        contenidos_no_eliminados = [contenido for contenido in contenidos_filtrados if not contenido.eliminado]

        if not contenidos_no_eliminados:
            return Response({"mensaje": "No hay contenidos para tus etiquetas favoritas."}, status=200)

        serializer = ContenidoSerializer(contenidos_no_eliminados, many=True, context={'request': request})
        return Response(serializer.data)


class RecomendacionesAleatoriasView(BaseContenidoView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recomendaciones = self.servicio.obtener_recomendaciones_aleatorias(cantidad=10)
        serializer = ContenidoSerializer(recomendaciones, many=True, context={'request': request})
        return Response(serializer.data)