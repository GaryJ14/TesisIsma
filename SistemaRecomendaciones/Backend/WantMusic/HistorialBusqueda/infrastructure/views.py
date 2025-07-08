from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Servicios y adaptadores
from Backend.WantMusic.HistorialBusqueda.infrastructure.repositories.historialBus_adapter import HistorialBusquedaAdapter
from Backend.WantMusic.HistorialBusqueda.applications.service.historialBus_service import HistorialBusquedaService

from Backend.WantMusic.Contenido.applications.service.contenido_service import ContenidoServicio
from Backend.TagWant.Etiqueta.applications.service.etiqueta_service import EtiquetaServicio

from Backend.WantMusic.Contenido.infrastructure.repositories.contenido_adapter import ContenidoAdapter
from Backend.TagWant.Etiqueta.infrastructure.repositories.etiqueta_adapter import EtiquetaAdapter
from Backend.TagWant.ContenidoEtiqueta.infrastructure.repositories.contenidoEti_adapter import ContenidoEtiquetaAdapter

from Backend.WantAdministrator.ContenidoEliminado.infrastructure.repositories.contenidoElim_adapter import ContenidoEliminadoAdapter
from Backend.WantMusic.UsuarioEtiquetasFavoritas.infrastructure.repositories.usuarioEtiFav_adapter import UsuarioEtiquetaFavoritaAdapter

from Backend.WantMusic.Contenido.infrastructure.serializers import ContenidoSerializer
from Backend.WantMusic.Usuario.infrastructure.repositories.usuario_adapter import UsuarioAdapter

class BuscarContenidoView(APIView):
    def get(self, request, query=None):
        if not query:
            return Response({"error": "No se proporcionó un término de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)

        # Repositorios
        contenido_repo = ContenidoAdapter()
        etiqueta_repo = EtiquetaAdapter()
        relacion_repo = ContenidoEtiquetaAdapter()
        contenido_eliminado_repo = ContenidoEliminadoAdapter()
        usuario_etiqueta_repo = UsuarioEtiquetaFavoritaAdapter()
        usuario_repo = UsuarioAdapter()  # ✅ Agregado

        # Servicio
        contenido_servicio = ContenidoServicio(
            contenido_repo,
            etiqueta_repo,
            relacion_repo,
            contenido_eliminado_repo,
            usuario_etiqueta_repo,
            usuario_repo  # ✅ Pasado al servicio
        )

        # Búsqueda
        contenidos = contenido_servicio.buscar_contenido(query)
        contenidos_no_eliminados = [c for c in contenidos if not c.eliminado]

        # Ya no hace falta este bloque manual
        # for c in contenidos_no_eliminados:
        #     ...

        # Registrar búsqueda
        if request.user.is_authenticated:
            historial_servicio = HistorialBusquedaService(HistorialBusquedaAdapter())
            historial_servicio.registrar_busqueda(request.user.id, query)

        # Serializar y responder
        serializer = ContenidoSerializer(contenidos_no_eliminados, many=True, context={'request': request})
        return Response(serializer.data)