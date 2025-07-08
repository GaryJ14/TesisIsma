from abc import ABC, abstractmethod
from typing import List
from Backend.TagWant.Etiqueta.domain.entities.etiqueta_model import Etiqueta

class EtiquetaPort(ABC):
    @abstractmethod
    def guardar(self, etiqueta: Etiqueta) -> Etiqueta: ...
    
    @abstractmethod
    def actualizar(self, etiqueta: Etiqueta) -> Etiqueta: ...

    @abstractmethod
    def obtener_por_id(self, id: int) -> Etiqueta: ...

    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Etiqueta: ...

    @abstractmethod
    def listar_todas(self) -> List[Etiqueta]: ...

    @abstractmethod
    def eliminar(self, id: int) -> None: ...
