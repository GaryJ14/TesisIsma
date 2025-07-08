from abc import ABC, abstractmethod

class EstadisticaUsuarioPort(ABC):
    @abstractmethod
    def guardar(self, estadistica): pass

    @abstractmethod
    def listar(self): pass

    @abstractmethod
    def obtener_por_id(self, id): pass

    @abstractmethod
    def eliminar(self, id): pass
