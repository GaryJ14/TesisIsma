from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Backend.AdministratorWant.EstadisticaUsuario.applications.service.estUsuario_service import EstadisticaUsuarioService
from Backend.AdministratorWant.EstadisticaUsuario.infrastructure.repositories.estUsuario_adapter import EstadisticaUsuarioAdapter

class EstadisticaDashboardView(APIView):
    def get(self, request):
        servicio = EstadisticaUsuarioService(EstadisticaUsuarioAdapter())

        # Guardar nueva estadística del día
        servicio.calcular_y_guardar_estadistica()

        estadisticas = servicio.listar()
        ultimas = sorted(estadisticas, key=lambda x: x.fecha_registro)[-30:]

        if not ultimas:
            return Response({"error": "No hay datos suficientes"}, status=404)

        # Listas separadas
        usuarios_totales = [e.total_usuarios for e in ultimas]
        usuarios_activos = [e.total_activos for e in ultimas]

        def calcular_tendencia(valores):
            return "up" if valores[-1] >= valores[0] else "down"

        return Response([
            {
                "title": "Usuarios Totales",
                "value": str(usuarios_totales[-1]),
                "interval": "Últimos 30 días",
                "trend": calcular_tendencia(usuarios_totales),
                "data": usuarios_totales
            },
            {
                "title": "Usuarios Activos",
                "value": str(usuarios_activos[-1]),
                "interval": "Últimos 30 días",
                "trend": calcular_tendencia(usuarios_activos),
                "data": usuarios_activos
            }
        ])
