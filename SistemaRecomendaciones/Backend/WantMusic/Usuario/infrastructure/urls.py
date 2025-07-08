from django.urls import path
from Backend.WantMusic.Usuario.infrastructure.views import *


urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('usuarios/', ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('perfil/', ObtenerUsuarioView.as_view(), name='obtener_usuario'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('actualizar/<int:id>/', ActualizarUsuarioView.as_view(), name='actualizar_usuario'),
    path('eliminar/<int:id>/', EliminarUsuarioView.as_view(), name='eliminar_usuario'),

]
