from abc import ABC, abstractmethod
from typing import List
from Backend.WantMusic.UsuarioEtiquetasFavoritas.domain.entities.usuarioEtiFav_model import UsuarioEtiquetaFavorita

class UsuarioEtiquetaFavoritaPort(ABC):
    @abstractmethod
    def agregar_favorita(self, favorita: UsuarioEtiquetaFavorita) -> UsuarioEtiquetaFavorita:
        pass

    @abstractmethod
    def eliminar_favorita(self, usuario_id: int, etiqueta_id: int) -> None:
        pass

    @abstractmethod
    def listar_favoritas_por_usuario(self, usuario_id: int) -> List[UsuarioEtiquetaFavorita]:
        pass

    @abstractmethod
    def listar_todas_favoritas(self) -> List[UsuarioEtiquetaFavorita]:
        pass
