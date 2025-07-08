from Backend.WantAdministrator.ContenidoEliminado.domain.entities.contenidoEli_model import ContenidoEliminado as ContenidoEliminadoEntidad
from Backend.WantAdministrator.ContenidoEliminado.infrastructure.models import ContenidoEliminado as ContenidoEliminadoModel
from Backend.WantAdministrator.ContenidoEliminado.domain.repositories.contenidoEli_port import ContenidoEliminadoPort

class ContenidoEliminadoAdapter(ContenidoEliminadoPort):

    def crear(self, entidad: ContenidoEliminadoEntidad):
        contenido_eliminado_model = ContenidoEliminadoModel(
            contenido_id=entidad.contenido_id,
            fecha_eliminacion=entidad.fecha_eliminacion,
            motivo=entidad.motivo,
            eliminado_por_id=entidad.eliminado_por_id
        )
        contenido_eliminado_model.save()
        return contenido_eliminado_model

    def listar_todos(self):
        modelos = ContenidoEliminadoModel.objects.all().order_by('-fecha_eliminacion')
        return [
            ContenidoEliminadoEntidad(
                id=m.id,
                contenido_id=m.contenido_id,
                fecha_eliminacion=m.fecha_eliminacion,
                motivo=m.motivo,
                eliminado_por_id=m.eliminado_por_id
            ) for m in modelos
        ]

    def obtener_por_id(self, id: int) -> ContenidoEliminadoEntidad:
        try:
            modelo = ContenidoEliminadoModel.objects.get(id=id)
            return self._mapear_a_entidad(modelo)
        except ContenidoEliminadoModel.DoesNotExist:
            raise Exception(f"Contenido eliminado con ID {id} no encontrado")

    def eliminar(self, id: int) -> None:
        try:
            modelo = ContenidoEliminadoModel.objects.get(id=id)
            modelo.delete()
        except ContenidoEliminadoModel.DoesNotExist:
            raise Exception(f"Contenido eliminado con ID {id} no encontrado")

    def _mapear_a_entidad(self, modelo: ContenidoEliminadoModel) -> ContenidoEliminadoEntidad:
        return ContenidoEliminadoEntidad(
            id=modelo.id,
            contenido_id=modelo.contenido_id,
            fecha_eliminacion=modelo.fecha_eliminacion,
            motivo=modelo.motivo,
            eliminado_por_id=modelo.eliminado_por_id
        )
