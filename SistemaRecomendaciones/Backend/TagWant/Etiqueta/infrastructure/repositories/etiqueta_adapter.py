# Infraestructura: repositories/etiqueta_adapter.py
from typing import List
from Backend.TagWant.Etiqueta.domain.entities.etiqueta_model import Etiqueta
from Backend.TagWant.Etiqueta.domain.repositories.Etiqueta_port import EtiquetaPort
from Backend.TagWant.Etiqueta.infrastructure.models import Etiqueta as EtiquetaModel

class EtiquetaAdapter(EtiquetaPort):

    def guardar(self, etiqueta: Etiqueta) -> Etiqueta:
        if etiqueta.id:
            try:
                etiqueta_model = EtiquetaModel.objects.get(id=etiqueta.id)
                etiqueta_model.nombre = etiqueta.nombre
                etiqueta_model.save()
            except EtiquetaModel.DoesNotExist:
                raise Exception("Etiqueta no encontrada para actualizar.")
        else:
            etiqueta_model = EtiquetaModel.objects.create(nombre=etiqueta.nombre)
        return Etiqueta(id=etiqueta_model.id, nombre=etiqueta_model.nombre)

    def obtener_por_id(self, id: int) -> Etiqueta | None:
        try:
            etiqueta_model = EtiquetaModel.objects.get(id=id)
            return Etiqueta(id=etiqueta_model.id, nombre=etiqueta_model.nombre)
        except EtiquetaModel.DoesNotExist:
            return None

    def obtener_por_nombre(self, nombre: str) -> Etiqueta | None:
        try:
            etiqueta_model = EtiquetaModel.objects.get(nombre=nombre)
            return Etiqueta(id=etiqueta_model.id, nombre=etiqueta_model.nombre)
        except EtiquetaModel.DoesNotExist:
            return None

    def listar_todas(self) -> List[Etiqueta]:
        return [Etiqueta(id=e.id, nombre=e.nombre) for e in EtiquetaModel.objects.only("id", "nombre").all()]

    def eliminar(self, id: int) -> None:
        if not EtiquetaModel.objects.filter(id=id).exists():
            raise Exception("Etiqueta no encontrada.")
        EtiquetaModel.objects.filter(id=id).delete()
    def actualizar(self, etiqueta: Etiqueta) -> Etiqueta:
        try:
            etiqueta_model = EtiquetaModel.objects.get(id=etiqueta.id)
            etiqueta_model.nombre = etiqueta.nombre
            etiqueta_model.save()
            return Etiqueta(id=etiqueta_model.id, nombre=etiqueta_model.nombre)
        except EtiquetaModel.DoesNotExist:
            raise Exception("Etiqueta no encontrada")
