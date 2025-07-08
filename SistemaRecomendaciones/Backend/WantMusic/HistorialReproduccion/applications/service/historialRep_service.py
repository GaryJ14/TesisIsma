from Backend.WantMusic.HistorialReproduccion.domain.entities.historialRep_model import HistorialReproduccion
from Backend.WantMusic.HistorialReproduccion.domain.repositories.historialRep_port import HistorialReproduccionPort
from Backend.WantMusic.Contenido.domain.repositories.contenido_port import ContenidoPort
from Backend.TagWant.ContenidoEtiqueta.domain.repositories.contenidoEti_port import ContenidoEtiquetaPort
from Backend.WantMusic.Usuario.domain.repositories.usuario_port import UsuarioPort  

class HistorialReproduccionService:
    def __init__(
        self,
        historial_repo: HistorialReproduccionPort,
        contenido_repo: ContenidoPort = None,
        relacion_repo: ContenidoEtiquetaPort = None,
        usuario_repo: UsuarioPort = None 
    ):
        self.historial_repo = historial_repo
        self.contenido_repo = contenido_repo
        self.relacion_repo = relacion_repo
        self.usuario_repo = usuario_repo  

    def agregar_historial(self, usuario_id: int, contenido_id: int, duracion_visto: int = None):
        historial = HistorialReproduccion(
            usuario_id=usuario_id,
            contenido_id=contenido_id,
            duracion_visto=duracion_visto
        )
        return self.historial_repo.agregar_historial(historial)

    def obtener_historial_usuario(self, usuario_id: int):
        return self.historial_repo.listar_por_usuario(usuario_id)

    def eliminar_historial(self, usuario_id: int, contenido_id: int) -> bool:
        return self.historial_repo.eliminar_historial(usuario_id, contenido_id)

    def eliminar_todo_historial(self, usuario_id: int):
        self.historial_repo.eliminar_todo(usuario_id)

    def obtener_historial_detallado(self, usuario_id: int):
        historial = self.historial_repo.listar_por_usuario(usuario_id)
        ids = [item.contenido_id for item in historial]
        contenidos = self.contenido_repo.obtener_por_ids(ids)

        for contenido in contenidos:
            # Etiquetas
            contenido.etiquetas = self.relacion_repo.obtener_etiquetas_por_contenido(contenido.id)

            # Fecha y duración
            match = next((h for h in historial if h.contenido_id == contenido.id), None)
            if match:
                contenido.fecha_reproduccion = match.fecha_reproduccion
                contenido.duracion_visto = match.duracion_visto

            # Nombre del usuario que subió el contenido
            if self.usuario_repo:
                usuario = self.usuario_repo.obtener_por_id(contenido.subido_por_id)
                contenido.subido_por_nombre = usuario.nombre if usuario else 'Anónimo'
            else:
                contenido.subido_por_nombre = 'Anónimo'

        return contenidos
