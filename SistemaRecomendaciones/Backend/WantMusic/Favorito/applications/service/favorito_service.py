from Backend.TagWant.ContenidoEtiqueta.domain.repositories.contenidoEti_port import ContenidoEtiquetaPort
from Backend.WantMusic.Favorito.domain.repositories.favorito_port import FavoritoPort
from Backend.WantMusic.Favorito.domain.entities.favorito_model import Favorito
from Backend.WantMusic.Contenido.domain.repositories.contenido_port import ContenidoPort
from Backend.WantMusic.Usuario.domain.repositories.usuario_port import UsuarioPort  
class FavoritoServicio:
    def __init__(
        self,
        repo: FavoritoPort,
        contenido_repo: ContenidoPort = None,
        relacion_repo: ContenidoEtiquetaPort = None,
        usuario_repo=None  
    ):
        self.repo = repo
        self.contenido_repo = contenido_repo
        self.relacion_repo = relacion_repo
        self.usuario_repo = usuario_repo

    def toggle_favorito(self, usuario_id: int, contenido_id: int):
        if self.repo.es_favorito(usuario_id, contenido_id):
            self.repo.eliminar(usuario_id, contenido_id)
            return "eliminado"
        else:
            favorito = Favorito(usuario_id, contenido_id)
            self.repo.agregar(favorito)
            return "agregado"

    def obtener_favoritos(self, usuario_id: int):
        favoritos = self.repo.listar_por_usuario(usuario_id)
        ids = [f.contenido_id for f in favoritos]
        contenidos = self.contenido_repo.obtener_por_ids(ids)

        for contenido in contenidos:
            if self.relacion_repo:
                contenido.etiquetas = self.relacion_repo.obtener_etiquetas_por_contenido(contenido.id)

            if self.usuario_repo:
                usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)
                contenido.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'
            else:
                contenido.subido_por_nombre = 'Anónimo'

        return contenidos

    def eliminar(self, usuario_id: int, contenido_id: int):
        self.repo.eliminar(usuario_id, contenido_id)
