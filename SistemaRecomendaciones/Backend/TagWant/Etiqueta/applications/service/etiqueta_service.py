from Backend.TagWant.Etiqueta.domain.repositories.Etiqueta_port import *
from Backend.WantMusic.Contenido.domain.repositories.contenido_port import ContenidoPort
from Backend.TagWant.Etiqueta.domain.entities.etiqueta_model import Etiqueta
from Backend.TagWant.ContenidoEtiqueta.domain.repositories.contenidoEti_port import ContenidoEtiquetaPort
class EtiquetaServicio:
    def __init__(self, etiqueta_repo: EtiquetaPort, contenido_repo: ContenidoPort, contenidoEti_repo: ContenidoEtiquetaPort):
        self.etiqueta_repo = etiqueta_repo
        self.contenido_repo = contenido_repo
        self.contenidoEti_repo = contenidoEti_repo

    def crear_etiqueta(self, nombre):
        nombre_normalizado = nombre.strip().lower()
        etiqueta_existente = self.etiqueta_repo.obtener_por_nombre(nombre_normalizado)
        if etiqueta_existente:
            raise Exception("La etiqueta ya existe")
        nueva_etiqueta = Etiqueta(nombre=nombre_normalizado)
        return self.etiqueta_repo.guardar(nueva_etiqueta)

    def obtener_etiqueta_por_id(self, id):
        etiqueta = self.etiqueta_repo.obtener_por_id(id)
        if not etiqueta:
            raise Exception("Etiqueta no encontrada")
        return etiqueta
    
    def listar_todas(self):
        return self.etiqueta_repo.listar_todas()

    def eliminar_etiqueta(self, id): 
        etiqueta = self.etiqueta_repo.obtener_por_id(id)
        if not etiqueta:
            raise Exception("Etiqueta no encontrada")
        self.etiqueta_repo.eliminar(id)

    def actualizar_etiqueta(self, id, nombre):
        etiqueta = self.etiqueta_repo.obtener_por_id(id)
        if not etiqueta:
            raise Exception("Etiqueta no encontrada")
        
        nombre_normalizado = nombre.strip().lower()
        etiqueta_existente = self.etiqueta_repo.obtener_por_nombre(nombre_normalizado)
        
        if etiqueta_existente and etiqueta_existente.id != id:
            raise Exception("La etiqueta ya existe con ese nombre")

        etiqueta.nombre = nombre_normalizado
        return self.etiqueta_repo.actualizar(etiqueta)

    def obtener_contenidos_por_etiqueta(self, etiqueta_id):
        return self.contenidoEti_repo.obtener_contenidos_por_etiqueta(etiqueta_id)
