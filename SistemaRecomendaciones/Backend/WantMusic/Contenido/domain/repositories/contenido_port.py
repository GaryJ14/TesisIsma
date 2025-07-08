from abc import ABC, abstractmethod
from typing import List, Optional
from Backend.WantMusic.Contenido.domain.entities.contenido_model import Contenido


class ContenidoPort(ABC):
    @abstractmethod
    def guardar(self, contenido: Contenido, archivo=None) -> Contenido:
        """Guarda un nuevo contenido o actualiza uno existente"""
        pass

    @abstractmethod
    def obtener_por_id(self, contenido_id: int) -> Optional[Contenido]:
        """Obtiene un contenido por su ID o retorna None si no existe"""
        pass


    @abstractmethod
    def listar_todos(self) -> List[Contenido]:
        """Retorna todos los contenidos"""
        pass

    @abstractmethod
    def listar_por_tipo(self, tipo: str) -> List[Contenido]:
        """Lista contenidos filtrando por tipo (audio/video)"""
        pass

    @abstractmethod
    def guardar_archivo_multimedia(self, tipo: str, archivo) -> str:
        """Guarda el archivo multimedia y retorna su ruta"""
        pass

    @abstractmethod
    def listar_eliminados(self) -> List[Contenido]:
        """Retorna los contenidos marcados como eliminados"""
        pass

    @abstractmethod
    def listar_contenidos_por_etiquetas(self, etiquetas_ids: List[int]) -> List[Contenido]:
        """Devuelve los contenidos relacionados con un conjunto de etiquetas"""
        pass
