from django.urls import path
from Backend.AdministratorWant.EstadisticaUsuario.infrastructure.views import *

urlpatterns = [
    path('estadisticas/dashboard/', EstadisticaDashboardView.as_view()),
]
