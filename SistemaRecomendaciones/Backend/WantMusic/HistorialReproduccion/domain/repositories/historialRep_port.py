from abc import ABC, abstractmethod
from Backend.WantMusic.HistorialReproduccion.domain.entities.historialRep_model import HistorialReproduccion
from typing import List

class HistorialReproduccionPort(ABC):
    @abstractmethod
    def agregar_historial(self, historial: HistorialReproduccion) -> HistorialReproduccion:
        pass

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[HistorialReproduccion]:
        pass    

    @abstractmethod
    def eliminar_historial(self, usuario_id: int, contenido_id: int) -> bool:
        pass

    @abstractmethod
    def eliminar_todo(self, usuario_id: int) -> bool:
        pass
