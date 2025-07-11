from datetime import datetime
from typing import List
from random import sample

from Backend.TagWant.ContenidoEtiqueta.domain.entities.contenidoEti_model import ContenidoEtiqueta
from Backend.TagWant.ContenidoEtiqueta.domain.repositories.contenidoEti_port import ContenidoEtiquetaPort
from Backend.WantMusic.Contenido.domain.entities.contenido_model import Contenido
from Backend.TagWant.Etiqueta.domain.entities.etiqueta_model import Etiqueta
from Backend.WantMusic.Contenido.domain.repositories.contenido_port import ContenidoPort
from Backend.TagWant.Etiqueta.domain.repositories.Etiqueta_port import EtiquetaPort
from Backend.WantAdministrator.ContenidoEliminado.domain.entities.contenidoEli_model import ContenidoEliminado as ContenidoEliminadoEntidad
from Backend.WantAdministrator.ContenidoEliminado.domain.repositories.contenidoEli_port import ContenidoEliminadoPort
from Backend.WantMusic.UsuarioEtiquetasFavoritas.domain.repositories.usuarioEtiFav_port import UsuarioEtiquetaFavoritaPort

class ContenidoServicio:
    def __init__(
        self,
        contenido_repo: ContenidoPort,
        etiqueta_repo: EtiquetaPort,
        repositorio_relacion: ContenidoEtiquetaPort,
        contenido_eliminado_repo: ContenidoEliminadoPort,
        usuario_etiqueta_repo=None,
        usuario_repo=None
    ):
        self.contenido_repo = contenido_repo
        self.etiqueta_repo = etiqueta_repo
        self.repositorio_relacion = repositorio_relacion
        self.contenido_eliminado_repo = contenido_eliminado_repo
        self.usuario_etiqueta_repo = usuario_etiqueta_repo
        self.usuario_repo = usuario_repo

    def crear_contenido_con_etiquetas(self, datos, archivo):
        contenido_dominio = Contenido(
            id=None,
            titulo=datos['titulo'],
            tipo=datos['tipo'],
            archivo='',
            subido_por_id=datos['subido_por_id'].id,
            artista=datos.get('artista', ''),
            fecha_subida=datetime.now(),
            eliminado=False
        )

        contenido_guardado = self.contenido_repo.guardar(contenido_dominio, archivo)

        etiquetas_nombres = datos.get('etiquetas', [])
        for nombre in etiquetas_nombres:
            nombre = nombre.strip().lower()
            etiqueta = self.etiqueta_repo.obtener_por_nombre(nombre)
            if not etiqueta:
                etiqueta = self.etiqueta_repo.guardar(Etiqueta(id=None, nombre=nombre))

            self.repositorio_relacion.crear(ContenidoEtiqueta(
                id=None,
                contenido_id=contenido_guardado.id,
                etiqueta_id=etiqueta.id
            ))

        contenido_guardado.etiquetas = self.repositorio_relacion.obtener_etiquetas_por_contenido(contenido_guardado.id)

        if self.usuario_repo:
            usuario = self.usuario_repo.obtener_por_id(contenido_guardado.subido_por_id)
            contenido_guardado.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'
        else:
            contenido_guardado.subido_por_nombre = 'Anónimo'

        return contenido_guardado

    def listar_contenidos(self):
        contenidos = self.contenido_repo.listar_todos()
        for contenido in contenidos:
            contenido.etiquetas = self.repositorio_relacion.obtener_etiquetas_por_contenido(contenido.id)
            if self.usuario_repo:
                usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)
                contenido.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'
            else:
                contenido.subido_por_nombre = 'Anónimo'
        return contenidos
    def listar_contenidos_por_usuario(self, usuario_id: int):
        contenidos = self.contenido_repo.listar_por_usuario(usuario_id)  # usa el método que agregaste al adapter

        for contenido in contenidos:
            contenido.etiquetas = self.repositorio_relacion.obtener_etiquetas_por_contenido(contenido.id)

            usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)
            contenido.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'

        return contenidos
    def obtener_contenido(self, contenido_id):
        contenido = self.contenido_repo.obtener_por_id(contenido_id)
        contenido.etiquetas = self.repositorio_relacion.obtener_etiquetas_por_contenido(contenido.id)

        if self.usuario_repo:
            usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)
            contenido.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'
        else:
            contenido.subido_por_nombre = 'Anónimo'

        return contenido

    def listar_por_tipo(self, tipo: str) -> List[Contenido]:
        if tipo not in ['audio', 'video']:
            return []
        return self.contenido_repo.listar_por_tipo(tipo)

    def actualizar_contenido(self, contenido, datos, archivo=None):
        contenido.titulo = datos.get('titulo', contenido.titulo)
        contenido.tipo = datos.get('tipo', contenido.tipo)
        contenido.artista = datos.get('artista', contenido.artista)

        if archivo:
            url_archivo = self.contenido_repo.guardar_archivo_multimedia(contenido.tipo, archivo)
            contenido.archivo = url_archivo

        contenido = self.contenido_repo.guardar(contenido)

        etiquetas_nombres = datos.get('etiquetas')
        if etiquetas_nombres is not None:
            relaciones_previas = self.repositorio_relacion.obtener_etiquetas_por_contenido(contenido.id)
            for etiqueta in relaciones_previas:
                self.repositorio_relacion.eliminar_relacion(contenido.id, etiqueta.id)

            for nombre in etiquetas_nombres:
                nombre_normalizado = nombre.strip().lower()
                etiqueta = self.etiqueta_repo.obtener_por_nombre(nombre_normalizado)
                if not etiqueta:
                    etiqueta = self.etiqueta_repo.guardar(Etiqueta(id=None, nombre=nombre_normalizado))
                self.repositorio_relacion.crear(ContenidoEtiqueta(
                    id=None,
                    contenido_id=contenido.id,
                    etiqueta_id=etiqueta.id
                ))

        contenido.etiquetas = self.repositorio_relacion.obtener_etiquetas_por_contenido(contenido.id)

        if self.usuario_repo:
            usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)
            contenido.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'
        else:
            contenido.subido_por_nombre = 'Anónimo'

        return contenido

    def eliminar_contenido(self, contenido_id: int, usuario_eliminador, motivo: str = None):
        contenido = self.contenido_repo.obtener_por_id(contenido_id)
        if not contenido:
            raise Exception("Contenido no encontrado")

        if contenido.eliminado:
            raise Exception("El contenido ya está eliminado")

        contenido.eliminado = True
        contenido.fecha_eliminacion = datetime.now()
        contenido.motivo_eliminacion = motivo
        self.contenido_repo.guardar(contenido)

        contenido_eliminado = ContenidoEliminadoEntidad(
            contenido_id=contenido.id,
            fecha_eliminacion=contenido.fecha_eliminacion,
            motivo=motivo,
            eliminado_por_id=usuario_eliminador.id 
        )
        self.contenido_eliminado_repo.crear(contenido_eliminado)

        return True 

    def buscar_contenido(self, query):
        resultados_titulo = self.contenido_repo.buscar_por_titulo(query)
        resultados_artista = self.contenido_repo.buscar_por_artista(query)

        etiqueta = self.etiqueta_repo.obtener_por_nombre(query.lower())
        if etiqueta:
            resultados_etiqueta = self.contenido_repo.listar_contenidos_por_etiquetas([etiqueta.id])
        else:
            resultados_etiqueta = []

        combinados = {c.id: c for c in (resultados_titulo + resultados_artista + resultados_etiqueta)}

        for contenido in combinados.values():
            contenido.etiquetas = self.repositorio_relacion.obtener_etiquetas_por_contenido(contenido.id)
            if self.usuario_repo:
                usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)
                contenido.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'
            else:
                contenido.subido_por_nombre = 'Anónimo'

        return list(combinados.values())

    def listar_contenidos_por_etiquetas(self, etiquetas_ids: list[int]):
        contenidos = self.contenido_repo.listar_contenidos_por_etiquetas(etiquetas_ids)
        for contenido in contenidos:
            contenido.etiquetas = self.repositorio_relacion.obtener_etiquetas_por_contenido(contenido.id)
            if self.usuario_repo:
                usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)
                contenido.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'
            else:
                contenido.subido_por_nombre = 'Anónimo'
        return contenidos

    def obtener_contenidos_recomendados(self, usuario_id: int):
        etiquetas_ids = self.obtener_etiquetas_favoritas(usuario_id)
        if not etiquetas_ids:
            return []

        contenidos = self.contenido_repo.listar_contenidos_por_etiquetas(etiquetas_ids)
        contenidos_filtrados = [c for c in contenidos if not c.eliminado]

        for contenido in contenidos_filtrados:
            contenido.etiquetas = self.repositorio_relacion.obtener_etiquetas_por_contenido(contenido.id)
            if self.usuario_repo:
                usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)
                contenido.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'
            else:
                contenido.subido_por_nombre = 'Anónimo'

        return contenidos_filtrados

    def obtener_contenido_con_etiquetas(self, contenido_id: int):
        contenido = self.contenido_repo.obtener_por_id(contenido_id)
        relaciones = self.repositorio_relacion.listar_todos()
        etiquetas_ids = [r.etiqueta_id for r in relaciones if r.contenido_id == contenido_id]
        etiquetas = [self.etiqueta_repo.obtener_por_id(eid) for eid in etiquetas_ids]

        if self.usuario_repo:
            usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)
            contenido.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'
        else:
            contenido.subido_por_nombre = 'Anónimo'

        return contenido, etiquetas

    def obtener_etiquetas_favoritas(self, usuario_id: int) -> List[int]:
        etiquetas = self.usuario_etiqueta_repo.listar_favoritas_por_usuario(usuario_id)
        return [e.etiqueta_id for e in etiquetas]

    def obtener_recomendaciones_aleatorias(self, cantidad=10) -> List[Contenido]:
        todos = self.contenido_repo.listar_todos()
        no_eliminados = [c for c in todos if not c.eliminado]
        for contenido in no_eliminados:
            contenido.etiquetas = self.repositorio_relacion.obtener_etiquetas_por_contenido(contenido.id)
            if self.usuario_repo:
                usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)
                contenido.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'
            else:
                contenido.subido_por_nombre = 'Anónimo'
        return sample(no_eliminados, min(cantidad, len(no_eliminados)))
