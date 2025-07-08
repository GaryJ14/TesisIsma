from datetime import timedelta
from pathlib import Path
import os
import dj_database_url

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# CONFIGURACIÓN SIMPLE SIN .ENV
# ============================================
# Detectar entorno por variable del sistema o por defecto desarrollo
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'development')
DEBUG = ENVIRONMENT == 'development'

# Clave secreta
if ENVIRONMENT == 'development':
    SECRET_KEY = 'clave-secreta-para-desarrollo-cambiar-en-produccion'
else:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'CAMBIAR-ESTA-CLAVE-EN-PRODUCCION')

# Hosts permitidos
if ENVIRONMENT == 'development':
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
else:
    # Para producción en tu servidor AlmaLinux
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
        # 'TU.IP.PUBLICA.AQUI',
    ]

# ============================================
# APLICACIONES
# ============================================
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

# ============================================
# MIDDLEWARE
# ============================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================
# CORS
# ============================================
if ENVIRONMENT == 'development':
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
    ]
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # Para producción - ajusta según necesites
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # Añade aquí las URLs de tu frontend cuando las tengas
    ]
    CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_CREDENTIALS = True

# ============================================
# BASE DE DATOS
# ============================================
if ENVIRONMENT == 'development':
    # PostgreSQL local en Windows
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'bddRecomendacionesVM',
            'USER': 'postgres',
            'PASSWORD': '123456',  # Cambia por tu contraseña local
            'HOST': 'localhost',
            'PORT': '5432',
            
        }
    }
else:
    # PostgreSQL en servidor AlmaLinux
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'bddRecomendacionesVM_prod'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'password_servidor'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'OPTIONS': {
                'connect_timeout': 20,
            }
        }
    }

# ============================================
# ARCHIVOS ESTÁTICOS Y MEDIA
# ============================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if ENVIRONMENT == 'development':
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================
# SEGURIDAD
# ============================================
if ENVIRONMENT == 'production':
    # Configuración básica de seguridad para servidor sin dominio
    SECURE_SSL_REDIRECT = False  # Sin SSL por ahora
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = False  # Sin HTTPS por ahora
    CSRF_COOKIE_SECURE = False
else:
    # Desarrollo - configuración relajada
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# ============================================
# REST FRAMEWORK + JWT
# ============================================
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

# ============================================
# GOOGLE DRIVE STORAGE CONFIGURATION
# ============================================
# Configuración de Google Drive Storage
DEFAULT_FILE_STORAGE = 'django_googledrive_storage.GoogleDriveStorage'

# Importar credenciales de Google Drive desde archivo separado
try:
    from .google_config import GOOGLE_DRIVE_CREDENTIALS
    GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = None
    GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS = GOOGLE_DRIVE_CREDENTIALS
    
    # Configuraciones de Google Drive
    GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = 'media/'
    GOOGLE_DRIVE_STORAGE_FILE_PERMISSIONS = 'anyoneWithLink'
    GOOGLE_DRIVE_STORAGE_MEDIA_FOLDER = '1Js7WVSK615274-txr1ozffwuU287k6ic'
    
    if ENVIRONMENT == 'development':
        print("✅ Google Drive configurado correctamente para DESARROLLO")
    else:
        print("✅ Google Drive configurado correctamente para PRODUCCIÓN")
        
except ImportError:
    # Fallback si no existe google_config.py
    print("⚠️  Advertencia: No se encontró google_config.py")
    print("   Google Drive Storage no funcionará. Crea el archivo google_config.py")
    
    # Configuración de fallback para archivos locales
    GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = None
    GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS = {}
    
    # Si no hay Google Drive, usar almacenamiento local
    if ENVIRONMENT == 'development':
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    else:
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# ============================================
# CONFIGURACIÓN BÁSICA
# ============================================
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

# ============================================
# DEBUG INFO - Solo en desarrollo
# ============================================
if ENVIRONMENT == 'development':
    print("="*50)
    print("🏠 ENTORNO: DESARROLLO")
    print(f"🗄️  Base de datos: {DATABASES['default']['NAME']}")
    print(f"📁 Storage: {DEFAULT_FILE_STORAGE}")
    print(f"🔧 Debug: {DEBUG}")
    print("="*50)
else:
    print("="*50)
    print("🚀 ENTORNO: PRODUCCIÓN")
    print(f"🗄️  Base de datos: {DATABASES['default']['NAME']}")
    print(f"📁 Storage: {DEFAULT_FILE_STORAGE}")
    print(f"🔧 Debug: {DEBUG}")
    print("="*50)