import random
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from Backend.WantMusic.Usuario.domain.entities.usuario_model import Usuario
from Backend.WantMusic.Usuario.domain.repositories.usuario_port import UsuarioPort
from Backend.WantMusic.Contenido.domain.repositories.contenido_port import ContenidoPort
from Backend.WantMusic.HistorialReproduccion.domain.repositories.historialRep_port import HistorialReproduccionPort

class UsuarioService:
    def __init__(self, usuario_repository, historial_repository, contenido_repository):
        self.usuario_repository = usuario_repository
        self.historial_repository = historial_repository
        self.contenido_repository = contenido_repository



    def registrar_usuario(self, nombre, email, password, foto_perfil=None):
        
        usuario = Usuario(
            id=None,
            nombre=nombre,
            email=email,
            password=password,
            foto_perfil=foto_perfil,
            is_active=True
        )
        return self.usuario_repository.guardar(usuario)

    def autenticar_usuario(self, email, password):
        usuario = self.usuario_repository.obtener_por_email(email)
        if usuario and check_password(password, usuario.password):
            return usuario
        return None

    def obtener_usuario_por_id(self, id):
        usuario = self.usuario_repository.obtener_por_id(id)
        if not usuario:
            raise Exception("Usuario no encontrado")
        return usuario

    def obtener_todos_usuarios(self):
        return self.usuario_repository.obtener_todos()

    def eliminar_usuario(self, id):
        usuario = self.usuario_repository.obtener_por_id(id)
        if not usuario:
            raise Exception("Usuario no encontrado")
        self.usuario_repository.eliminar(id)

    def actualizar_usuario(self, id, nombre, email, password, is_active, foto_perfil=None):
        usuario = self.usuario_repository.obtener_por_id(id)
        if not usuario:
            raise Exception("Usuario no encontrado")

        usuario.nombre = nombre
        usuario.email = email
        usuario.password = make_password(password)  # cifrar de nuevo
        usuario.foto_perfil = foto_perfil
        usuario.is_active = is_active

        return self.usuario_repository.actualizar(usuario)

    def suspender_usuario(self, usuario_id):
        usuario = self.usuario_repository.obtener_por_id(usuario_id)
        if not usuario:
            raise Exception("Usuario no encontrado")
        usuario.is_active = False
        return self.usuario_repository.actualizar(usuario)
        return self.historial_repo.agregar_historial(historial)

    def tokens_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
