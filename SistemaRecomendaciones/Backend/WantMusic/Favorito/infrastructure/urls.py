from django.urls import path
from Backend.WantMusic.Favorito.infrastructure.views import ToggleFavoritoView, ListarFavoritosView, EliminarFavoritoView

urlpatterns = [
    path('favoritos/', ListarFavoritosView.as_view()),
    path('favoritos/toggle/<int:contenido_id>/', ToggleFavoritoView.as_view()),
    path('favoritos/eliminar/<int:contenido_id>/', EliminarFavoritoView.as_view()),
]
