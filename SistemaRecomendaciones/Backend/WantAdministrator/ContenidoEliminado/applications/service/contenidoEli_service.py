# Se crea el servicio de la aplicación, que contiene la lógica de negocio y se comunica con los repositorios.
# No accede a modelos de Django, solo usa la interfaz WantMusicRepositorioPort. 
#PARTE 3

import datetime
from typing import List
from Backend.WantAdministrator.ContenidoEliminado.domain.entities.contenidoEli_model import ContenidoEliminado
from Backend.WantAdministrator.ContenidoEliminado.domain.repositories.contenidoEli_port import ContenidoEliminadoPort
from Backend.WantMusic.Contenido.domain.repositories.contenido_port import ContenidoPort
from Backend.TagWant.Etiqueta.domain.repositories.Etiqueta_port import EtiquetaPort
from Backend.TagWant.ContenidoEtiqueta.domain.repositories.contenidoEti_port import ContenidoEtiquetaPort
from Backend.WantMusic.Usuario.domain.repositories.usuario_port import UsuarioPort
class ContenidoEliminadoServicio:
    def __init__(self, repo: ContenidoEliminadoPort, contenido_repo: ContenidoPort, etiqueta_repo: EtiquetaPort,
                 relacion_repo: ContenidoEtiquetaPort, usuario_repo: UsuarioPort):
        self.repo = repo
        self.contenido_repo = contenido_repo
        self.etiqueta_repo = etiqueta_repo
        self.relacion_repo = relacion_repo
        self.usuario_repo = usuario_repo

    def crear_eliminacion(self, entidad: ContenidoEliminado):
        # Aquí la fecha se puede establecer antes o al crear la entidad
        if entidad.fecha_eliminacion is None:
            entidad.fecha_eliminacion = datetime.now()
        return self.repo.crear(entidad)
    def listar_eliminados(self) -> List[ContenidoEliminado]:
        return self.repo.listar_todos()

    def obtener_eliminado(self, id: int) -> ContenidoEliminado:
        return self.repo.obtener_por_id(id)

    def eliminar_registro(self, id: int) -> None:
        self.repo.eliminar(id)

    def listar_eliminados_enriquecidos(self, request=None):
        eliminados = self.repo.listar_todos()
        resultado = []

        for elim in eliminados:
            contenido = self.contenido_repo.obtener_por_id(elim.contenido_id)
            if not contenido:
                continue

            etiquetas = self.relacion_repo.obtener_etiquetas_por_contenido(contenido.id)
            usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)

            # 🔥 aquí construimos la URL absoluta del archivo
            archivo_url = contenido.archivo
            if archivo_url and not archivo_url.startswith('http'):
                archivo_url = archivo_url.lstrip('/')  # quita slashes duplicados
                archivo_url = request.build_absolute_uri(f"/{archivo_url}") if request else f"/media/{archivo_url}"

            resultado.append({
                "id": elim.id,
                "contenido_id": contenido.id,
                "titulo": contenido.titulo,
                "tipo": contenido.tipo,
                "archivo": archivo_url,
                "artista": contenido.artista,
                "etiquetas": [{"id": e.id, "nombre": e.nombre} for e in etiquetas],
                "subido_por_nombre": usuario.nombre if usuario else "Anónimo",
                "fecha_subida": contenido.fecha_subida.isoformat() if contenido.fecha_subida else None,
                "fecha_eliminacion": elim.fecha_eliminacion.isoformat(),
                "motivo_eliminacion": elim.motivo,
            })

        return resultado
