from typing import List, Optional
from Backend.WantMusic.Usuario.infrastructure.models import Usuario as DjangoUser
from Backend.WantMusic.Usuario.domain.entities.usuario_model import Usuario
from Backend.WantMusic.Usuario.domain.repositories.usuario_port import UsuarioPort


class UsuarioAdapter(UsuarioPort):

    @staticmethod
    def to_domain(user: DjangoUser) -> Usuario:
        return Usuario(
            id=user.id,
            nombre=user.nombre,
            email=user.email,
            password=user.password,
            foto_perfil=user.foto_perfil,  
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser
        )

    @staticmethod
    def to_django(usuario: Usuario) -> DjangoUser:
        user = DjangoUser(
            id=usuario.id,
            nombre=usuario.nombre,
            email=usuario.email,
            is_active=usuario.is_active,
            is_staff=usuario.is_staff,
            is_superuser=usuario.is_superuser,
            foto_perfil=usuario.foto_perfil
        )
        user.set_password(usuario.password)
        return user

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        try:
            user = DjangoUser.objects.get(email=email)
            return self.to_domain(user)
        except DjangoUser.DoesNotExist:
            return None

    def guardar(self, usuario: Usuario) -> Usuario:
        user = self.to_django(usuario)
        user.save()
        return self.to_domain(user)

    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        try:
            user = DjangoUser.objects.get(id=id)
            return self.to_domain(user)
        except DjangoUser.DoesNotExist:
            return None

    def obtener_todos(self) -> List[Usuario]:
        return [self.to_domain(user) for user in DjangoUser.objects.all()]

    def eliminar(self, id: int) -> None:
        deleted, _ = DjangoUser.objects.filter(id=id).delete()
        if deleted == 0:
            raise Exception("Usuario no encontrado")

    def actualizar(self, usuario: Usuario) -> Usuario:
        try:
            user = DjangoUser.objects.get(id=usuario.id)
            user.nombre = usuario.nombre
            user.email = usuario.email
            if usuario.password:
                user.set_password(usuario.password)
            user.foto_perfil = usuario.foto_perfil
            user.is_active = usuario.is_active
            user.is_staff = usuario.is_staff
            user.is_superuser = usuario.is_superuser
            user.save()
            return self.to_domain(user)
        except DjangoUser.DoesNotExist:
            raise Exception("Usuario no encontrado")
