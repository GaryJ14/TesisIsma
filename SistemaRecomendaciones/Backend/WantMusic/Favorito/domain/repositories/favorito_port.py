from abc import ABC, abstractmethod
from typing import List
from Backend.WantMusic.Favorito.domain.entities.favorito_model import Favorito

class FavoritoPort(ABC):
    @abstractmethod
    def agregar(self, favorito: Favorito) -> Favorito:
        pass

    @abstractmethod
    def eliminar(self, usuario_id: int, contenido_id: int) -> None:
        pass

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[Favorito]:
        pass

    @abstractmethod
    def es_favorito(self, usuario_id: int, contenido_id: int) -> bool:
        pass
