from Backend.WantMusic.UsuarioEtiquetasFavoritas.domain.entities.usuarioEtiFav_model import UsuarioEtiquetaFavorita as Entidad
from Backend.WantMusic.UsuarioEtiquetasFavoritas.domain.repositories.usuarioEtiFav_port import UsuarioEtiquetaFavoritaPort
from Backend.WantMusic.UsuarioEtiquetasFavoritas.infrastructure.models import UsuarioEtiquetaFavorita as Modelo

class UsuarioEtiquetaFavoritaAdapter(UsuarioEtiquetaFavoritaPort):

    def agregar_favorita(self, favorita: Entidad) -> Entidad:
        modelo = Modelo.objects.create(
            usuario_id=favorita.usuario_id,
            etiqueta_id=favorita.etiqueta_id
        )
        return Entidad(modelo.usuario_id, modelo.etiqueta_id)

    def eliminar_favorita(self, usuario_id: int, etiqueta_id: int):
        Modelo.objects.filter(usuario_id=usuario_id, etiqueta_id=etiqueta_id).delete()

    def listar_favoritas_por_usuario(self, usuario_id: int):
        return [
            Entidad(m.usuario_id, m.etiqueta_id)
            for m in Modelo.objects.filter(usuario_id=usuario_id)
        ]

    def listar_todas_favoritas(self):
        return [
            Entidad(m.usuario_id, m.etiqueta_id)
            for m in Modelo.objects.all()
        ]
    def listar_favoritas_por_usuario(self, usuario_id: int):
        return list(Modelo.objects.filter(usuario_id=usuario_id))