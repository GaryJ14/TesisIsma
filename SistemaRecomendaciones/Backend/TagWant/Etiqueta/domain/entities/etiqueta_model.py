class Etiqueta:
    def __init__(self, nombre: str, id: int = None):
        self.id = id
        self.nombre = nombre

    def __str__(self):
        return self.nombre