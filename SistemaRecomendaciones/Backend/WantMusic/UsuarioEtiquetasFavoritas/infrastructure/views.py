from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from Backend.WantMusic.UsuarioEtiquetasFavoritas.infrastructure.repositories.usuarioEtiFav_adapter import UsuarioEtiquetaFavoritaAdapter
from Backend.WantMusic.UsuarioEtiquetasFavoritas.applications.service.usuarioEtiFav_service import UsuarioEtiquetaFavoritaServicio

class ListarEtiquetasFavoritasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        servicio = UsuarioEtiquetaFavoritaServicio(UsuarioEtiquetaFavoritaAdapter())
        favoritas = servicio.obtener_favoritas(request.user.id)
        data = [{"usuario_id": f.usuario_id, "etiqueta_id": f.etiqueta_id} for f in favoritas]
        return Response(data)

class CrearEtiquetaFavoritaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        servicio = UsuarioEtiquetaFavoritaServicio(UsuarioEtiquetaFavoritaAdapter())
        etiquetas_ids = request.data.get("etiquetas_ids", [])
        errores = []
        for eid in etiquetas_ids:
            try:
                servicio.agregar_favorita(request.user.id, eid)
            except Exception as e:
                errores.append(str(e))
        if errores:
            return Response({"errores": errores}, status=status.HTTP_207_MULTI_STATUS)
        return Response({"mensaje": "Favoritas agregadas"}, status=status.HTTP_201_CREATED)


class EliminarEtiquetaFavoritaView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):  # <-- aquí debe aceptar `id`
        usuario = request.user
        repo = UsuarioEtiquetaFavoritaAdapter()
        servicio = UsuarioEtiquetaFavoritaServicio(repo)
        try:
            servicio.eliminar_favorita(usuario.id, id)
            return Response({"mensaje": "Etiqueta favorita eliminada"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class ActualizarEtiquetaFavoritaView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        usuario_id = request.user.id
        etiqueta_vieja = request.data.get('etiqueta_vieja')
        etiqueta_nueva = request.data.get('etiqueta_nueva')

        if not etiqueta_vieja or not etiqueta_nueva:
            return Response(
                {"error": "Los campos 'etiqueta_vieja' y 'etiqueta_nueva' son requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        repo = UsuarioEtiquetaFavoritaAdapter()
        servicio = UsuarioEtiquetaFavoritaServicio(repo)

        try:
            servicio.actualizar_favorita(usuario_id, int(etiqueta_vieja), int(etiqueta_nueva))
            return Response({"mensaje": "Etiqueta favorita actualizada correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)