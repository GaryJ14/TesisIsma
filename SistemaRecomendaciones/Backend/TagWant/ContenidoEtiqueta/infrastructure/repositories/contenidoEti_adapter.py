from django.db import IntegrityError
from Backend.TagWant.ContenidoEtiqueta.domain.entities.contenidoEti_model import ContenidoEtiqueta
from Backend.TagWant.ContenidoEtiqueta.domain.repositories.contenidoEti_port import ContenidoEtiquetaPort
from Backend.TagWant.ContenidoEtiqueta.infrastructure.models import ContenidoEtiqueta as ContenidoEtiquetaModel
from Backend.TagWant.Etiqueta.infrastructure.models import Etiqueta as EtiquetaModel
from Backend.TagWant.Etiqueta.domain.entities.etiqueta_model import Etiqueta
from Backend.WantMusic.Contenido.infrastructure.models import Contenido
class ContenidoEtiquetaAdapter(ContenidoEtiquetaPort):
    from django.db import IntegrityError

    def crear(self, relacion: ContenidoEtiqueta) -> ContenidoEtiqueta:
        try:
            obj, _ = ContenidoEtiquetaModel.objects.get_or_create(
                contenido_id=relacion.contenido_id,
                etiqueta_id=relacion.etiqueta_id
            )
            return ContenidoEtiqueta(id=obj.id, contenido_id=obj.contenido_id, etiqueta_id=obj.etiqueta_id)
        except IntegrityError:
            # Puedes devolver una excepción más explícita o ignorar si ya existe
            raise Exception("La relación ya existe")


    def obtener_por_id(self, id: int) -> ContenidoEtiqueta:
        obj = ContenidoEtiquetaModel.objects.get(id=id)
        return ContenidoEtiqueta(id=obj.id, contenido_id=obj.contenido_id, etiqueta_id=obj.etiqueta_id)

    def listar_todos(self):
        return [ContenidoEtiqueta(id=o.id, contenido_id=o.contenido_id, etiqueta_id=o.etiqueta_id)
                for o in ContenidoEtiquetaModel.objects.all()]

    def eliminar(self, id: int) -> None:
            ContenidoEtiquetaModel.objects.filter(id=id).delete()
    def eliminar_relacion(self, contenido_id: int, etiqueta_id: int):
        """Elimina la relación entre un contenido y una etiqueta"""
        ContenidoEtiquetaModel.objects.filter(
            contenido_id=contenido_id, 
            etiqueta_id=etiqueta_id
        ).delete()
    def obtener_etiquetas_por_contenido(self, contenido_id: int) -> list[Etiqueta]:
        relaciones = ContenidoEtiquetaModel.objects.filter(contenido_id=contenido_id).select_related("etiqueta")
        return [Etiqueta(id=r.etiqueta.id, nombre=r.etiqueta.nombre) for r in relaciones]


    def obtener_contenidos_por_etiqueta(self, etiqueta_id: int):
        relaciones = ContenidoEtiquetaModel.objects.filter(etiqueta_id=etiqueta_id)
        contenido_ids = [rel.contenido_id for rel in relaciones]
        contenidos = Contenido.objects.filter(id__in=contenido_ids)

        # Si necesitas mapear a entidades de dominio, hazlo aquí:
        return list(contenidos)
