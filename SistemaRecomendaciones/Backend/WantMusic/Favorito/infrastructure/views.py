from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from Backend.WantMusic.Favorito.applications.service.favorito_service import FavoritoServicio
from Backend.WantMusic.Favorito.infrastructure.repositories.favorito_adapter import FavoritoAdapter
from Backend.WantMusic.Favorito.infrastructure.serializers import FavoritoSerializer

from Backend.WantMusic.Contenido.infrastructure.serializers import ContenidoSerializer
from Backend.WantMusic.Contenido.infrastructure.repositories.contenido_adapter import ContenidoAdapter
from Backend.TagWant.ContenidoEtiqueta.infrastructure.repositories.contenidoEti_adapter import ContenidoEtiquetaAdapter
from Backend.WantMusic.Usuario.infrastructure.repositories.usuario_adapter import UsuarioAdapter 

class ToggleFavoritoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, contenido_id):
        servicio = FavoritoServicio(FavoritoAdapter())
        estado = servicio.toggle_favorito(request.user.id, contenido_id)
        return Response({"status": estado}, status=200)


class ListarFavoritosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        servicio = FavoritoServicio(
            FavoritoAdapter(),
            contenido_repo=ContenidoAdapter(),
            relacion_repo=ContenidoEtiquetaAdapter(),
            usuario_repo=UsuarioAdapter()  
        )
        favoritos = servicio.obtener_favoritos(request.user.id)
        serializer = ContenidoSerializer(favoritos, many=True)
        return Response(serializer.data)


class EliminarFavoritoView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, contenido_id):
        servicio = FavoritoServicio(FavoritoAdapter())
        servicio.eliminar(request.user.id, contenido_id)
        return Response({"mensaje": "Favorito eliminado"}, status=204)
