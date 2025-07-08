from Backend.AdministratorWant.EstadisticaFavorito.domain.entities.estFavorito_model import EstadisticaFavorito
from Backend.AdministratorWant.EstadisticaFavorito.domain.repositories.estFavorito_port import EstadisticaFavoritoPort
from Backend.WantMusic.Favorito.infrastructure.models import Favorito

class EstadisticaFavoritoService:
    def __init__(self, repo: EstadisticaFavoritoPort):
        self.repo = repo

    def calcular_y_guardar_estadistica(self):
        total = Favorito.objects.count()
        estadistica = EstadisticaFavorito(
            total_contenidos=total
        )
        return self.repo.guardar(estadistica)

    def listar(self):
        return self.repo.listar()

    def eliminar(self, id):
        self.repo.eliminar(id)
