from abc import ABC, abstractmethod
from typing import List
from Backend.TagWant.ContenidoEtiqueta.domain.entities.contenidoEti_model import ContenidoEtiqueta
from Backend.TagWant.Etiqueta.domain.entities.etiqueta_model import Etiqueta
class ContenidoEtiquetaPort(ABC):
    @abstractmethod
    def crear(self, relacion: ContenidoEtiqueta) -> ContenidoEtiqueta:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> ContenidoEtiqueta:
        pass

    @abstractmethod
    def listar_todos(self) -> List[ContenidoEtiqueta]:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> None:
        pass
    @abstractmethod
    def obtener_etiquetas_por_contenido(self, contenido_id: int) -> list[Etiqueta]:
        """Devuelve todas las etiquetas asociadas a un contenido"""
        pass
