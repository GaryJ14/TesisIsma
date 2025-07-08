
# --- /infrastructure/repositories/estFavorito_adapter.py ---
from Backend.AdministratorWant.EstadisticaFavorito.domain.entities.estFavorito_model import EstadisticaFavorito as FavoritoEntidad
from Backend.AdministratorWant.EstadisticaFavorito.domain.repositories.estFavorito_port import EstadisticaFavoritoPort
from Backend.AdministratorWant.EstadisticaFavorito.infrastructure.models import EstadisticaFavorito as FavoritoModelo
from Backend.WantMusic.Favorito.infrastructure.models import Favorito

class EstadisticaFavoritoAdapter(EstadisticaFavoritoPort):
    def guardar(self, estadistica: FavoritoEntidad):
        model = FavoritoModelo.objects.create(
            etiqueta=estadistica.etiqueta,
            total_contenidos=estadistica.total_contenidos
        )
        return FavoritoEntidad(
            id=model.id,
            etiqueta=model.etiqueta,
            total_contenidos=model.total_contenidos,
            fecha_registro=model.fecha_registro
        )

    def listar(self):
        return [
            FavoritoEntidad(
                id=m.id,
                etiqueta=m.etiqueta,
                total_contenidos=m.total_contenidos,
                fecha_registro=m.fecha_registro
            ) for m in FavoritoModelo.objects.all().order_by('-fecha_registro')
        ]

    def eliminar(self, id):
        FavoritoModelo.objects.filter(id=id).delete()

