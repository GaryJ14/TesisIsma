#Interfaz que abstrae las operaciones sobre usuarios:
#Define la interfaz (puerto) del repositorio que usará el servicio. PASO 2
from abc import ABC, abstractmethod
from typing import List
from Backend.WantAdministrator.ContenidoEliminado.domain.entities.contenidoEli_model import ContenidoEliminado

class ContenidoEliminadoPort(ABC):
    @abstractmethod
    def crear(self, entidad: ContenidoEliminado):
        """Registrar la eliminación de contenido en el historial."""
        pass

    @abstractmethod
    def listar_todos(self):
        """Listar todas las eliminaciones."""
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> ContenidoEliminado:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> None:
        pass

