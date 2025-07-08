class Favorito:
    def __init__(self, usuario_id: int, contenido_id: int, fecha_favorito=None):
        self.usuario_id = usuario_id
        self.contenido_id = contenido_id
        self.fecha_favorito = fecha_favorito
