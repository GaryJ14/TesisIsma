from Backend.WantMusic.Favorito.domain.entities.favorito_model import Favorito
from Backend.WantMusic.Favorito.domain.repositories.favorito_port import FavoritoPort
from Backend.WantMusic.Favorito.infrastructure.models import Favorito as FavoritoModel

class FavoritoAdapter(FavoritoPort):
    def agregar(self, favorito: Favorito) -> Favorito:
        modelo, _ = FavoritoModel.objects.get_or_create(
            usuario_id=favorito.usuario_id,
            contenido_id=favorito.contenido_id
        )
        return self._mapear_a_entidad(modelo)

    def eliminar(self, usuario_id: int, contenido_id: int) -> None:
        FavoritoModel.objects.filter(usuario_id=usuario_id, contenido_id=contenido_id).delete()

    def listar_por_usuario(self, usuario_id: int):
        modelos = FavoritoModel.objects.filter(usuario_id=usuario_id)
        return [self._mapear_a_entidad(m) for m in modelos]

    def es_favorito(self, usuario_id: int, contenido_id: int) -> bool:
        return FavoritoModel.objects.filter(usuario_id=usuario_id, contenido_id=contenido_id).exists()

    def _mapear_a_entidad(self, modelo):
        return Favorito(
            usuario_id=modelo.usuario_id,
            contenido_id=modelo.contenido_id,
            fecha_favorito=modelo.fecha_favorito
        )
