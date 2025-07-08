from django.urls import include, path
from Backend.WantMusic.HistorialBusqueda.infrastructure.views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# Create a router for ContenidoMultimediaViewSet
router = DefaultRouter()

urlpatterns = [
    #BUSQUEDA
    path('contenidos/buscar/<str:query>/', BuscarContenidoView.as_view(), name='buscar_contenido'),

]