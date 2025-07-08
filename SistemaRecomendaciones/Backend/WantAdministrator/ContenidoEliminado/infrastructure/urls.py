# UrlWantAdministrator
from django.urls import include, path
from Backend.WantAdministrator.ContenidoEliminado.infrastructure.views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# Create a router for ContenidoMultimediaViewSet
router = DefaultRouter()

urlpatterns = [
    path('contenidos/eliminados/', ListarEliminadosView.as_view(), name='contenidos-eliminados'),
]