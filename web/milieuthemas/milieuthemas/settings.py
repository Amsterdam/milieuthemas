# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

from datapunt_generic.generic.database import get_docker_host, in_docker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIVA_DIR = os.path.abspath(os.path.join(BASE_DIR, './', 'diva'))

DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, './', 'data'))

OVERRIDE_HOST_ENV_VAR = 'DATABASE_HOST_OVERRIDE'
OVERRIDE_PORT_ENV_VAR = 'DATABASE_PORT_OVERRIDE'

DATAPUNT_API_URL = os.getenv(
    'DATAPUNT_API_URL', 'https://api.datapunt.amsterdam.nl/')

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

if TESTING:
    DATA_DIR = DIVA_DIR

default_secret = "default-secret"
SECRET_KEY = os.getenv("SECRET_KEY", default_secret)
DEBUG = SECRET_KEY == default_secret

ALLOWED_HOSTS = ['*']


class LocationKey:
    local = 'local'
    docker = 'docker'
    override = 'override'


def get_database_key():
    if os.getenv(OVERRIDE_HOST_ENV_VAR):
        return LocationKey.override
    elif in_docker():
        return LocationKey.docker

    return LocationKey.local


# Application definition

PROJECT_APPS = [
    'atlas',
    'geo_views',
    'atlas_api',
    'datasets.themas',
    'datasets.schiphol',
    'datasets.bodeminformatie',
    'datasets.geluidzone',
    'datasets.veiligheidsafstanden',
    'datasets.risicozones_bedrijven',
    'datasets.risicozones_infrastructuur',
    'datasets.bommenkaart',
    'datapunt_generic.batch',
    'datapunt_generic.generic',
    'datapunt_generic.health',
]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
    'django.contrib.sites',

    'django.contrib.gis',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework_gis',
    ] + PROJECT_APPS

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ROOT_URLCONF = 'milieuthemas.urls'

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

WSGI_APPLICATION = 'milieuthemas.wsgi.application'

DATABASE_OPTIONS = {
    LocationKey.docker: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'milieuthemas'),
        'USER': os.getenv('DATABASE_USER', 'milieuthemas'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': 'database',
        'PORT': '5432'
    },
    LocationKey.local: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'milieuthemas'),
        'USER': os.getenv('DATABASE_USER', 'milieuthemas'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': get_docker_host(),
        'PORT': '5402'
    },
    LocationKey.override: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'milieuthemas'),
        'USER': os.getenv('DATABASE_USER', 'milieuthemas'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': os.getenv(OVERRIDE_HOST_ENV_VAR),
        'PORT': os.getenv(OVERRIDE_PORT_ENV_VAR, '5432')
    },
}

DATABASES = {
    'default': DATABASE_OPTIONS[get_database_key()]
}

BATCH_SETTINGS = dict(
    batch_size=100000
)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))

LOGGING = {

    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'console': {
            'format': '%(asctime)s - %(name)20s - %(levelname)s - %(message)s',
        },
    },

    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },

    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },

        'batch': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    },
}

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'

INTERNAL_IPS = ['127.0.0.1']

REST_FRAMEWORK = dict(
    PAGE_SIZE=25,
    MAX_PAGINATE_BY=100,
    DEFAULT_AUTHENTICATION_CLASSES=(
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    DEFAULT_PAGINATION_CLASS='drf_hal_json.pagination.HalPageNumberPagination',
    DEFAULT_PARSER_CLASSES=(
        'drf_hal_json.parsers.JsonHalParser',
    ),
    DEFAULT_RENDERER_CLASSES=(
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    DEFAULT_FILTER_BACKENDS=(
        'django_filters.rest_framework.DjangoFilterBackend',
    )
)

CORS_ORIGIN_REGEX_WHITELIST = (
    '^(https?://)?localhost(:\d+)?$',
    '^(https?://)?.*\.datalabamsterdam\.nl$',
    '^(https?://)?.*\.amsterdam\.nl$',
)

# Security

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
# CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

HEALTH_MODEL = 'schiphol.HoogtebeperkendeVlakken'
