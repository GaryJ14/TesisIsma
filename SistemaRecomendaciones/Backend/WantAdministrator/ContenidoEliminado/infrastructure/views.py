from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Backend.WantAdministrator.ContenidoEliminado.applications.service.contenidoEli_service import ContenidoEliminadoServicio
from Backend.WantAdministrator.ContenidoEliminado.infrastructure.repositories.contenidoElim_adapter import ContenidoEliminadoAdapter
from Backend.WantAdministrator.ContenidoEliminado.infrastructure.serializers import ContenidoEliminadoSerializer
from Backend.WantAdministrator.ContenidoEliminado.domain.entities.contenidoEli_model import ContenidoEliminado

from Backend.TagWant.ContenidoEtiqueta.infrastructure.repositories.contenidoEti_adapter import ContenidoEtiquetaAdapter
from Backend.TagWant.Etiqueta.infrastructure.repositories.etiqueta_adapter import EtiquetaAdapter
from Backend.WantMusic.Contenido.infrastructure.repositories.contenido_adapter import ContenidoAdapter
from Backend.WantMusic.Usuario.infrastructure.repositories.usuario_adapter import UsuarioAdapter

class ListarEliminadosView(APIView):
    def get(self, request):
        servicio = ContenidoEliminadoServicio(
            ContenidoEliminadoAdapter(),
            ContenidoAdapter(),
            EtiquetaAdapter(),
            ContenidoEtiquetaAdapter(),
            UsuarioAdapter()
        )

        eliminados = servicio.listar_eliminados_enriquecidos(request=request)  # ← pasa el request
        return Response(eliminados, status=status.HTTP_200_OK)
