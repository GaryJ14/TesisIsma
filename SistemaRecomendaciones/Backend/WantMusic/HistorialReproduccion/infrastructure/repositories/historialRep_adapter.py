from Backend.WantMusic.HistorialReproduccion.domain.entities.historialRep_model import HistorialReproduccion
from Backend.WantMusic.HistorialReproduccion.domain.repositories.historialRep_port import HistorialReproduccionPort
from Backend.WantMusic.HistorialReproduccion.infrastructure.models import HistorialReproduccion as HistorialReproduccionModel

class HistorialReproduccionAdapter(HistorialReproduccionPort):
    def agregar_historial(self, historial: HistorialReproduccion) -> HistorialReproduccion:
        historial_model = HistorialReproduccionModel.objects.create(
            usuario_id=historial.usuario_id,
            contenido_id=historial.contenido_id,
            duracion_visto=historial.duracion_visto
        )
        return self._mapear_a_entidad(historial_model)

    def listar_por_usuario(self, usuario_id: int):
        historial_models = HistorialReproduccionModel.objects.filter(usuario_id=usuario_id)
        return [self._mapear_a_entidad(h) for h in historial_models]

   
    def eliminar_historial(self, usuario_id: int, contenido_id: int) -> bool:
        eliminados, _ = HistorialReproduccionModel.objects.filter(
            usuario_id=usuario_id,
            contenido_id=contenido_id
        ).delete()
        return eliminados > 0


    def eliminar_todo(self, usuario_id: int):
        HistorialReproduccionModel.objects.filter(usuario_id=usuario_id).delete()
        return True
    
    def _mapear_a_entidad(self, modelo: HistorialReproduccionModel) -> HistorialReproduccion:
        return HistorialReproduccion(
            usuario_id=modelo.usuario_id,
            contenido_id=modelo.contenido_id,
            fecha_reproduccion=modelo.fecha_reproduccion,
            duracion_visto=modelo.duracion_visto
        )
