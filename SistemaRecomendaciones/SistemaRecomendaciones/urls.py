"""
URL configuration for SistemaRecomendaciones project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Backend.WantMusic.Usuario.infrastructure.urls')),
    path('api/', include('Backend.WantMusic.Contenido.infrastructure.urls')),
    path('api/', include('Backend.WantMusic.UsuarioEtiquetasFavoritas.infrastructure.urls')),
    path('api/', include('Backend.WantMusic.Favorito.infrastructure.urls')),
    path('api/', include('Backend.WantMusic.HistorialReproduccion.infrastructure.urls')),
    path('api/', include('Backend.WantMusic.HistorialBusqueda.infrastructure.urls')),
    
    path('api/', include('Backend.WantAdministrator.ContenidoEliminado.infrastructure.urls')),
    
    path('api/', include('Backend.TagWant.Etiqueta.infrastructure.urls')),
    path('api/', include('Backend.TagWant.ContenidoEtiqueta.infrastructure.urls')),
    
    path('api/', include('Backend.AdministratorWant.EstadisticaUsuario.infrastructure.urls')),
    path('api/', include('Backend.AdministratorWant.EstadisticaFavorito.infrastructure.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)