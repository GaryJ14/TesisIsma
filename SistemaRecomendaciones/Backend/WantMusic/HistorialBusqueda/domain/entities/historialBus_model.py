from datetime import datetime

class HistorialBusqueda:
    def __init__(self, usuario_id, termino_busqueda, fecha_busqueda=None):
        self.usuario_id = usuario_id
        self.termino_busqueda = termino_busqueda
        self.fecha_busqueda = fecha_busqueda or datetime.now()
