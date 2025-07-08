from Backend.AdministratorWant.EstadisticaUsuario.domain.entities.estUsuario_model import EstadisticaUsuario
from Backend.AdministratorWant.EstadisticaUsuario.domain.repositories.estUsuario_port import EstadisticaUsuarioPort
from django.contrib.auth import get_user_model

User = get_user_model()

class EstadisticaUsuarioService:
    def __init__(self, repo: EstadisticaUsuarioPort):
        self.repo = repo

    def calcular_y_guardar_estadistica(self):
        total = User.objects.count()
        activos = User.objects.filter(is_active=True).count()

        estadistica = EstadisticaUsuario(
            total_usuarios=total,
            total_activos=activos
        )
        return self.repo.guardar(estadistica)

    def listar(self):
        return self.repo.listar()
