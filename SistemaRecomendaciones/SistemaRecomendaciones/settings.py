from datetime import timedelta
from pathlib import Path
import os
import dj_database_url  # ✅ Importante para Heroku DATABASE_URL

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = [
    'apisound-bd202b4fd327.herokuapp.com',
    'localhost',
    '127.0.0.1'
]

# Archivos estáticos y media
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    # Apps propias
    'Backend.WantMusic.Contenido.infrastructure.apps.ContenidoInfraConfig',
    'Backend.WantMusic.Favorito.infrastructure.apps.FavoritoInfraConfig',
    'Backend.WantMusic.HistorialBusqueda.infrastructure.apps.HistorialBusqInfraConfig',
    'Backend.WantMusic.HistorialReproduccion.infrastructure.apps.HistorialRepInfraConfig',
    'Backend.WantMusic.Usuario.infrastructure.apps.UsuarioInfraConfig',
    'Backend.WantMusic.UsuarioEtiquetasFavoritas.infrastructure.apps.UsuarioEtiFavInfraConfig',
    'Backend.WantAdministrator.ContenidoEliminado.infrastructure.apps.ContenidoEliminadoInfraConfig',
    'Backend.TagWant.ContenidoEtiqueta.infrastructure.apps.ContenidoEtiquetaInfraConfig',
    'Backend.TagWant.Etiqueta.infrastructure.apps.EtiquetaInfraConfig',
    'Backend.AdministratorWant.EstadisticaFavorito.infrastructure.apps.EstFavoritoInfraConfig',
    'Backend.AdministratorWant.EstadisticaUsuario.infrastructure.apps.EstUsuarioInfraConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS = True

# REST framework + JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}

# Seguridad básica (puedes mejorar en producción)
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Usuario personalizado
AUTH_USER_MODEL = 'Usuario_infrastructure.Usuario'

ROOT_URLCONF = 'SistemaRecomendaciones.urls'
WSGI_APPLICATION = 'SistemaRecomendaciones.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Base de datos por defecto (para local)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bddRecomendacionesVM',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ✅ Reemplazar config local si Heroku proporciona DATABASE_URL
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES["default"] = dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de Google Drive Storage
DEFAULT_FILE_STORAGE = 'django_googledrive_storage.GoogleDriveStorage'

GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = os.path.join(BASE_DIR, 'credenciales-drive.json')  # Ruta a tu archivo descargado
GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = 'media/'
GOOGLE_DRIVE_STORAGE_FILE_PERMISSIONS = 'anyoneWithLink' # Permisos para los archivos subidos
GOOGLE_DRIVE_STORAGE_MEDIA_FOLDER = '1Js7WVSK615274-txr1ozffwuU287k6ic'  # ID de la carpeta en Drive donde se guardarán los archivos

