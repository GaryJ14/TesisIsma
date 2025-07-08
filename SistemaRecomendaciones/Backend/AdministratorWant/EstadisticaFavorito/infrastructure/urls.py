from django.urls import path
from Backend.AdministratorWant.EstadisticaFavorito.infrastructure.views import EstadisticaFavoritosDashboardView

urlpatterns = [
    path('favoritos/dashboard/', EstadisticaFavoritosDashboardView.as_view()),
]
