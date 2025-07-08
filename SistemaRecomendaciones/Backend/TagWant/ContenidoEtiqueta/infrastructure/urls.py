from django.urls import path
from Backend.TagWant.ContenidoEtiqueta.infrastructure.views import (
    CrearContenidoEtiquetaView,
    ListarContenidoEtiquetaView,
    EliminarContenidoEtiquetaView,
)

urlpatterns = [
    path('relaciones/', ListarContenidoEtiquetaView.as_view(), name='listar_relaciones'),
    path('relaciones/crear/', CrearContenidoEtiquetaView.as_view(), name='crear_relacion'),
    path('relaciones/eliminar/<int:id>/', EliminarContenidoEtiquetaView.as_view(), name='eliminar_relacion'),
]
