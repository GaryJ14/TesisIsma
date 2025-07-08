from abc import ABC, abstractmethod

class EstadisticaFavoritoPort(ABC):
    @abstractmethod
    def guardar(self, estadistica): pass

    @abstractmethod
    def listar(self): pass

    @abstractmethod
    def eliminar(self, id): pass