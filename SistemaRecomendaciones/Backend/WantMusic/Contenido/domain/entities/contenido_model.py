# contenido_model.py
class Contenido:
    def __init__(self, id, titulo, tipo, archivo, fecha_subida, subido_por_id, artista, eliminado):
        self.id = id
        self.titulo = titulo
        self.tipo = tipo
        self.archivo = archivo
        self.fecha_subida = fecha_subida
        self.subido_por_id = subido_por_id
        self.artista = artista
        self.eliminado = eliminado
        self.etiquetas = []  # esto debe llenarse

    def get_nombres_etiquetas(self):
        return [etiqueta.nombre for etiqueta in self.etiquetas]
