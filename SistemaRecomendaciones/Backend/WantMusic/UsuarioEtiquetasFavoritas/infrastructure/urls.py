from django.urls import include, path
from Backend.WantMusic.UsuarioEtiquetasFavoritas.infrastructure.views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# Create a router for ContenidoMultimediaViewSet
router = DefaultRouter()

urlpatterns = [

   #Etiquetas Favoritas
    path('usuario/etiquetas-favoritas/', ListarEtiquetasFavoritasView.as_view(), name='listar_etiquetas_favoritas'),  # GET
    path('usuario/etiquetas-favoritas/crear/', CrearEtiquetaFavoritaView.as_view(), name='crear_etiqueta_favorita'),  # POST
    path('usuario/etiquetas-favoritas/actualizar/', ActualizarEtiquetaFavoritaView.as_view()),
    path('usuario/etiquetas-favoritas/eliminar/<int:id>/', EliminarEtiquetaFavoritaView.as_view(), name='eliminar_etiqueta_favorita'),  # DELETE
   
]