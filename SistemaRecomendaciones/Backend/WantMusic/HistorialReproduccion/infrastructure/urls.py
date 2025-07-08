from django.urls import include, path
from Backend.WantMusic.HistorialReproduccion.infrastructure.views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# Create a router for ContenidoMultimediaViewSet
router = DefaultRouter()

urlpatterns = [
    # Historial de Reproducción
    path('historial/', HistorialReproduccionView.as_view(), name='historial_reproduccion'),
    path('eliminarhistorial/<int:contenido_id>/', EliminarHistorial.as_view()),
    path('eliminarTodohistorial/', EliminarTodoHistorial.as_view(), name='eliminar_todo_historial'),
]