from Backend.TagWant.ContenidoEtiqueta.domain.entities.contenidoEti_model import ContenidoEtiqueta


class ContenidoEtiquetaServicio:
    def __init__(self, contenido_etiqueta_repo):
        self.repo = contenido_etiqueta_repo

    def crear_relacion(self, contenido_id, etiqueta_id):
        relacion = ContenidoEtiqueta(contenido_id=contenido_id, etiqueta_id=etiqueta_id)
        return self.repo.crear(relacion)

    def listar(self):
        return self.repo.listar_todos()

    def obtener(self, id):
        return self.repo.obtener_por_id(id)

    def eliminar(self, id):
        return self.repo.eliminar(id)
