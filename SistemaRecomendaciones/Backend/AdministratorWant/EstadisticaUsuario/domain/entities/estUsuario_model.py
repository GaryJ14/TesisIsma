from datetime import datetime

class EstadisticaUsuario:
    def __init__(self, id=None, total_usuarios=0, total_activos=0, fecha_registro=None):
        self.id = id
        self.total_usuarios = total_usuarios
        self.total_activos = total_activos
        self.fecha_registro = fecha_registro or datetime.now()
