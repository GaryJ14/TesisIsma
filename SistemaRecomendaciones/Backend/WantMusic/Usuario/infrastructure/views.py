
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from Backend.WantMusic.Usuario.applications.services.usuario_service import UsuarioService
from Backend.WantMusic.Usuario.infrastructure.repositories.usuario_adapter import UsuarioAdapter
from Backend.WantMusic.Usuario.infrastructure.serializers import UsuarioSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            foto_perfil = request.FILES.get("foto_perfil", None)

            servicio = UsuarioService(UsuarioAdapter(), None, None)
            usuario = servicio.registrar_usuario(
                nombre=data["nombre"],
                email=data["email"],
                password=data["password"],
                foto_perfil=foto_perfil
            )

            tokens = servicio.tokens_user(usuario)

            return Response({
                "mensaje": "Usuario registrado exitosamente",
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"],
                "id": usuario.id,
                "email": usuario.email,
                "nombre": usuario.nombre,
                "foto_perfil": usuario.foto_perfil.url if usuario.foto_perfil else None
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListaUsuariosView(ListAPIView):
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        servicio = UsuarioService(UsuarioAdapter(), None, None)
        return servicio.obtener_todos_usuarios()


class ObtenerUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            servicio = UsuarioService(UsuarioAdapter(), None, None)
            usuario = servicio.obtener_usuario_por_id(request.user.id)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class LoginUsuarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email y contraseña son obligatorios"}, status=400)

        servicio = UsuarioService(UsuarioAdapter(), None, None)
        usuario = servicio.autenticar_usuario(email, password)
        if usuario:
            tokens = servicio.tokens_user(usuario)
            return Response({
                "message": "Inicio de sesión exitoso",
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"],
                "id": usuario.id,
                "email": usuario.email,
                "nombre": usuario.nombre,
                "foto_perfil": usuario.foto_perfil.url if usuario.foto_perfil else None,
                "role": (
                    "superadmin" if usuario.is_superuser else
                    "admin" if usuario.is_staff else
                    "usuario"
                )
            }, status=200)
        else:
            return Response({"error": "Email y/o contraseña incorrectos"}, status=401)


class ActualizarUsuarioView(APIView):
    def put(self, request, id):
        data = request.data
        foto = request.FILES.get("foto_perfil", None)
        servicio = UsuarioService(UsuarioAdapter(), None, None)

        try:
            servicio.actualizar_usuario(
                id=id,
                nombre=data["nombre"],
                email=data["email"],
                password=data.get("password"),
                is_active=data.get("is_active", True),
                foto_perfil=foto
            )
            return Response({"mensaje": "Usuario actualizado correctamente"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class EliminarUsuarioView(APIView):
    def delete(self, request, id):
        servicio = UsuarioService(UsuarioAdapter(), None, None)
        try:
            servicio.eliminar_usuario(id)
            return Response({"mensaje": "Usuario eliminado exitosamente"}, status=204)
        except Exception as e:
            return Response({"error": str(e)}, status=404)
