# Backend/WantMusic/Contenido/infrastructure/urls.py
from django.urls import path
from Backend.WantMusic.Contenido.infrastructure.views import *

urlpatterns = [
    path('contenidos/', ListarContenidoView.as_view(), name='listar_contenidos'),
    path('contenidos/crear/', CrearContenidoView.as_view(), name='crear_contenido'),
    path('contenidos/actualizar/<int:pk>/', ActualizarContenidoView.as_view(), name='actualizar_contenido'),
    path('contenidos/eliminar/<int:pk>/', EliminarContenidoView.as_view(), name='eliminar_contenido'),
    
    
    
    #RECOMENDACIONES POR ETIQUETAS
    path('contenidos/por-etiquetas-favoritas/', ContenidosPorEtiquetasFavoritasView.as_view(), name='contenidos_por_etiquetas_favoritas'),

    #ALEATORIAS
    path('recomendaciones/', RecomendacionesAleatoriasView.as_view(), name='recomendaciones'),
    
]
