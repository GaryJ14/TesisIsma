from dataclasses import dataclass
from datetime import datetime

@dataclass
class EstadisticaFavorito:
    id: int = None
    etiqueta: str = "Mis Favoritos"
    total_contenidos: int = 0
    fecha_registro: datetime = None
