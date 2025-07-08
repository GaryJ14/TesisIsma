from Backend.WantMusic.HistorialBusqueda.domain.entities.historialBus_model import HistorialBusqueda
from Backend.WantMusic.HistorialBusqueda.domain.repositories.historialBus_port import HistorialBusquedaPort
from Backend.WantMusic.HistorialBusqueda.infrastructure.models import HistorialBusqueda

class HistorialBusquedaAdapter(HistorialBusquedaPort):
    def guardar(self, historial: HistorialBusqueda) -> HistorialBusqueda:
        model = HistorialBusqueda.objects.create(
            usuario_id=historial.usuario_id,
            termino_busqueda=historial.termino_busqueda,
            fecha_busqueda=historial.fecha_busqueda
        )
        return HistorialBusqueda(
            usuario_id=model.usuario_id,
            termino_busqueda=model.termino_busqueda,
            fecha_busqueda=model.fecha_busqueda
        )

    def listar_por_usuario(self, usuario_id: int):
        modelos = HistorialBusqueda.objects.filter(usuario_id=usuario_id).order_by('-fecha_busqueda')
        return [
            HistorialBusqueda(
                usuario_id=m.usuario_id,
                termino_busqueda=m.termino_busqueda,
                fecha_busqueda=m.fecha_busqueda
            ) for m in modelos
        ]
