from Backend.AdministratorWant.EstadisticaUsuario.domain.entities.estUsuario_model import EstadisticaUsuario
from Backend.AdministratorWant.EstadisticaUsuario.domain.repositories.estUsuario_port import EstadisticaUsuarioPort
from Backend.AdministratorWant.EstadisticaUsuario.infrastructure.models import EstadisticaUsuario as EstadisticaUsuarioModel

class EstadisticaUsuarioAdapter(EstadisticaUsuarioPort):
    def guardar(self, estadistica: EstadisticaUsuario):
        model = EstadisticaUsuarioModel.objects.create(
            total_usuarios=estadistica.total_usuarios,
            total_activos=estadistica.total_activos
        )
        return EstadisticaUsuario(
            id=model.id,
            total_usuarios=model.total_usuarios,
            total_activos=model.total_activos,
            fecha_registro=model.fecha_registro
        )

    def listar(self):
        return [
            EstadisticaUsuario(
                id=m.id,
                total_usuarios=m.total_usuarios,
                total_activos=m.total_activos,
                fecha_registro=m.fecha_registro
            )
            for m in EstadisticaUsuarioModel.objects.all().order_by('-fecha_registro')
        ]

    def obtener_por_id(self, id):
        try:
            m = EstadisticaUsuarioModel.objects.get(id=id)
            return EstadisticaUsuario(
                id=m.id,
                total_usuarios=m.total_usuarios,
                total_activos=m.total_activos,
                fecha_registro=m.fecha_registro
            )
        except EstadisticaUsuarioModel.DoesNotExist:
            return None

    def eliminar(self, id):
        EstadisticaUsuarioModel.objects.filter(id=id).delete()
