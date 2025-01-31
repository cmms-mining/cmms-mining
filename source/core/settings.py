import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

if os.path.exists('/.dockerenv'):
    DOCKER_MODE = True
else:
    DOCKER_MODE = False

if not DOCKER_MODE:
    load_dotenv(os.path.join(BASE_DIR.parent, 'environment', '.env.dev-local'))


SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [os.getenv('CSRF_TRUSTED_ORIGINS')]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'axes',
    'debug_toolbar',
    'storages',

    'apps.accounts',
    'apps.backoffice',
    'apps.buckets',
    'apps.common',
    'apps.components',
    'apps.contractors',
    'apps.documents',
    'apps.db_logger',
    'apps.equip_documents',
    'apps.equipments',
    'apps.firefighting',
    'apps.importer',
    'apps.maintenance',
    'apps.sites',
    'apps.tasks',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    'middleware.LoginRequiredMiddleware',

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


if DOCKER_MODE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        },
    }
if not DOCKER_MODE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Asia/Yekaterinburg"

USE_I18N = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

if DOCKER_MODE:
    STATIC_ROOT = '/var/www/static'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
if DOCKER_MODE:
    MEDIA_ROOT = '/var/www/uploads'

MEDIA_URL = '/uploads/'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'

AXES_FAILURE_LIMIT = 500
AXES_LOCKOUT_TEMPLATE = 'login.html'

AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',

    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

if os.getenv('UPLOAD') == 's3':
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_FILES_OVERWRITE = False
    AWS_S3_REGION_NAME = "us-east-1"
    AWS_DEFAULT_ACL = None
    AWS_S3_SIGNATURE_NAME = "s3v4"
    AWS_S3_VERITY = True

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            },
    }

INTERNAL_IPS = [
    "127.0.0.1",
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'apps.db_logger.db_log_handler.DatabaseLogHandler',
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['db_log'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# Установить время жизни сессии при бездействии — 2 часа (в секундах)
SESSION_COOKIE_AGE = 2 * 60 * 60  # 2 часа
SESSION_SAVE_EVERY_REQUEST = True  # Обновлять сессию при каждом запросе

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

TELEGRAM_BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_USER_ID = os.getenv('USER_ID')
