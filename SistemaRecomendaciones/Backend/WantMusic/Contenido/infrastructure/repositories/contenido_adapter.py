import os
import datetime
from typing import List
from django.core.files.storage import default_storage
from django.conf import settings
from django.utils import timezone

from Backend.WantMusic.Contenido.infrastructure.models import Contenido as ContenidoModel
from Backend.WantAdministrator.ContenidoEliminado.infrastructure.models import ContenidoEliminado
from Backend.WantMusic.Contenido.domain.entities.contenido_model import Contenido as ContenidoDominio


class ContenidoAdapter:

    def guardar(self, contenido_dominio: ContenidoDominio, archivo=None) -> ContenidoDominio:
        if contenido_dominio.id:
            try:
                contenido_model = ContenidoModel.objects.get(id=contenido_dominio.id)
            except ContenidoModel.DoesNotExist:
                raise Exception("Contenido no encontrado para actualizar.")
        else:
            contenido_model = ContenidoModel()

        contenido_model.titulo = contenido_dominio.titulo
        contenido_model.tipo = contenido_dominio.tipo
        contenido_model.artista = contenido_dominio.artista
        contenido_model.subido_por_id = contenido_dominio.subido_por_id
        contenido_model.eliminado = contenido_dominio.eliminado

        if archivo:
            contenido_model.archivo = archivo

        contenido_model.save()

        return self._mapear_a_entidad(contenido_model)

    def eliminar(self, contenido_id: int, motivo: str = "") -> bool:
        try:
            contenido = ContenidoModel.objects.get(id=contenido_id)

            contenido_eliminado = ContenidoEliminado(
                contenido=contenido,
                motivo_eliminacion=motivo,
                fecha_eliminacion=timezone.now()
            )
            contenido_eliminado.save()

            contenido.eliminado = True
            contenido.fecha_eliminacion = timezone.now()
            contenido.save()

            return True
        except ContenidoModel.DoesNotExist:
            raise Exception("Contenido no encontrado")

    def obtener_por_id(self, contenido_id: int) -> ContenidoDominio | None:
        try:
            contenido_model = ContenidoModel.objects.get(id=contenido_id)
            return self._mapear_a_entidad(contenido_model)
        except ContenidoModel.DoesNotExist:
            return None
    def obtener_por_ids(self, ids: list[int]) -> List[ContenidoDominio]:
        modelos = ContenidoModel.objects.filter(id__in=ids, eliminado=False)
        return [self._mapear_a_entidad(m) for m in modelos]


    def listar_todos(self) -> List[ContenidoDominio]:
        modelos = ContenidoModel.objects.filter(eliminado=False)
        return [self._mapear_a_entidad(m) for m in modelos]
    def listar_por_usuario(self, usuario_id: int) -> List[ContenidoDominio]:
        modelos = ContenidoModel.objects.filter(subido_por_id=usuario_id, eliminado=False).order_by('-fecha_subida')
        return [self._mapear_a_entidad(m) for m in modelos]
    def listar_por_tipo(self, tipo: str) -> List[ContenidoDominio]:
        return [
            self._mapear_a_entidad(c)
            for c in ContenidoModel.objects.filter(tipo=tipo, eliminado=False).order_by('-fecha_subida')
        ]

    def buscar_por_titulo(self, query):
        modelos = ContenidoModel.objects.filter(titulo__icontains=query, eliminado=False)
        return [self._mapear_a_entidad(m) for m in modelos]

    def buscar_por_artista(self, query):
        modelos = ContenidoModel.objects.filter(artista__icontains=query, eliminado=False)
        return [self._mapear_a_entidad(m) for m in modelos]


    def listar_eliminados(self) -> List[ContenidoDominio]:
        eliminados = ContenidoEliminado.objects.select_related('contenido').all().order_by('-fecha_eliminacion')
        return [self._mapear_eliminado(e) for e in eliminados]

    def listar_contenidos_por_etiquetas(self, etiquetas_ids: list[int]) -> List[ContenidoDominio]:
        modelos = ContenidoModel.objects.filter(
            relaciones_etiquetas__etiqueta_id__in=etiquetas_ids,
            eliminado=False
        ).distinct()
        return [self._mapear_a_entidad(m) for m in modelos]

    def buscar_por_titulo(self, query: str) -> List[ContenidoDominio]:
        modelos = ContenidoModel.objects.filter(titulo__icontains=query, eliminado=False)
        return [self._mapear_a_entidad(m) for m in modelos]

    def buscar_por_artista(self, query: str) -> List[ContenidoDominio]:
        modelos = ContenidoModel.objects.filter(artista__icontains=query, eliminado=False)
        return [self._mapear_a_entidad(m) for m in modelos]

    def guardar_archivo_multimedia(self, tipo: str, archivo) -> str:
        hoy = datetime.date.today()
        subcarpeta = f"{hoy.year}/{hoy.month:02d}"
        ruta_carpeta = os.path.join(settings.MEDIA_ROOT, tipo, subcarpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)

        nombre_archivo = archivo.name
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)

        if not default_storage.exists(ruta_completa):
            with default_storage.open(ruta_completa, 'wb+') as destino:
                for chunk in archivo.chunks():
                    destino.write(chunk)

        ruta_relativa = os.path.join(tipo, subcarpeta, nombre_archivo).replace("\\", "/")
        return ruta_relativa

    def _mapear_a_entidad(self, contenido_model: ContenidoModel) -> ContenidoDominio:
        return ContenidoDominio(
            id=contenido_model.id,
            titulo=contenido_model.titulo,
            tipo=contenido_model.tipo,
            archivo=contenido_model.archivo.url if contenido_model.archivo else '',
            subido_por_id=contenido_model.subido_por_id,
            artista=contenido_model.artista,
            fecha_subida=contenido_model.fecha_subida,
            eliminado=contenido_model.eliminado
        )

    def _mapear_eliminado(self, eliminado_model: ContenidoEliminado) -> ContenidoDominio:
        contenido = eliminado_model.contenido
        entidad = self._mapear_a_entidad(contenido)
        entidad.eliminado = True
        entidad.fecha_eliminacion = eliminado_model.fecha_eliminacion
        entidad.motivo_eliminacion = eliminado_model.motivo
        return entidad
