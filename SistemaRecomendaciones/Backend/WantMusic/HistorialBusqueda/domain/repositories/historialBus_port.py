from abc import ABC, abstractmethod
from typing import List
from Backend.WantMusic.HistorialBusqueda.domain.entities.historialBus_model import HistorialBusqueda

class HistorialBusquedaPort(ABC):
    @abstractmethod
    def guardar(self, historial: HistorialBusqueda) -> HistorialBusqueda:
        pass

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[HistorialBusqueda]:
        pass
