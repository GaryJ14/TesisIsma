# Backend/WantAdministrator/ContenidoEliminado/domain/entities/contenidoEli_model.py
from datetime import datetime

class ContenidoEliminado:
    def __init__(self, contenido_id: int, fecha_eliminacion: datetime, motivo: str, eliminado_por_id: int, id: int = None):
        self.id = id
        self.contenido_id = contenido_id
        self.fecha_eliminacion = fecha_eliminacion
        self.motivo = motivo
        self.eliminado_por_id = eliminado_por_id
