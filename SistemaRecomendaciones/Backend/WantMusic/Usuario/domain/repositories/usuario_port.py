from abc import ABC, abstractmethod
from typing import List
from Backend.WantMusic.Usuario.domain.entities.usuario_model import Usuario

class UsuarioPort(ABC):

    @abstractmethod
    def obtener_por_email(self, email: str) -> Usuario:
        pass

    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Usuario:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Usuario]:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> None:
        pass

    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario:
        pass
