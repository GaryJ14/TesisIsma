
from Backend.WantMusic.HistorialBusqueda.domain.entities.historialBus_model import HistorialBusqueda
from Backend.WantMusic.HistorialBusqueda.infrastructure.repositories.historialBus_adapter import HistorialBusquedaAdapter


class HistorialBusquedaService:
    def __init__(self, historial_repo):
        self.historial_repo = historial_repo

    def registrar_busqueda(self, usuario_id, termino_busqueda):
        historial = HistorialBusqueda(usuario_id=usuario_id, termino_busqueda=termino_busqueda)
        return self.historial_repo.guardar(historial)

    def obtener_historial_usuario(self, usuario_id):
        return self.historial_repo.listar_por_usuario(usuario_id)
