from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Backend.AdministratorWant.EstadisticaFavorito.applications.service.estFavorito_service import EstadisticaFavoritoService
from Backend.AdministratorWant.EstadisticaFavorito.infrastructure.repositories.estFavorito_adapter import EstadisticaFavoritoAdapter

class EstadisticaFavoritosDashboardView(APIView):
    def get(self, request):
        servicio = EstadisticaFavoritoService(EstadisticaFavoritoAdapter())

        # Calcula y guarda estadística del día
        servicio.calcular_y_guardar_estadistica()

        estadisticas = servicio.listar()
        ultimas = sorted(estadisticas, key=lambda x: x.fecha_registro)[-30:]

        if not ultimas:
            return Response({"error": "No hay datos suficientes"}, status=status.HTTP_404_NOT_FOUND)

        valores = [e.total_contenidos for e in ultimas]
        tendencia = "up" if valores[-1] >= valores[0] else "down"
        total = valores[-1]
        total_texto = f"{total}k" if total >= 1000 else str(total)

        return Response({
            "title": "Favoritos",
            "value": total_texto,
            "interval": "Últimos 30 días",
            "trend": tendencia,
            "data": valores
        })
