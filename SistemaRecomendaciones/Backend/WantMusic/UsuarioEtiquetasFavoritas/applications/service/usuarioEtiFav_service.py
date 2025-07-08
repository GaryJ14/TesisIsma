from Backend.WantMusic.UsuarioEtiquetasFavoritas.domain.repositories.usuarioEtiFav_port import UsuarioEtiquetaFavoritaPort
from Backend.WantMusic.UsuarioEtiquetasFavoritas.domain.entities.usuarioEtiFav_model import UsuarioEtiquetaFavorita

class UsuarioEtiquetaFavoritaServicio:
    def __init__(self, repo: UsuarioEtiquetaFavoritaPort):
        self.repo = repo

    def obtener_favoritas(self, usuario_id: int):
        return self.repo.listar_favoritas_por_usuario(usuario_id)

    def agregar_favorita(self, usuario_id: int, etiqueta_id: int):
        favorita = UsuarioEtiquetaFavorita(usuario_id, etiqueta_id)
        return self.repo.agregar_favorita(favorita)

    def eliminar_favorita(self, usuario_id: int, etiqueta_id: int):
        self.repo.eliminar_favorita(usuario_id, etiqueta_id)

    def actualizar_favorita(self, usuario_id: int, etiqueta_id_vieja: int, etiqueta_id_nueva: int):
        self.repo.eliminar_favorita(usuario_id, etiqueta_id_vieja)
        favorita_nueva = UsuarioEtiquetaFavorita(usuario_id, etiqueta_id_nueva)
        return self.repo.agregar_favorita(favorita_nueva)
