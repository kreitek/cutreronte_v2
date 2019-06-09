"""
Django settings for cutreronte_v2 project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#5zx8m5-ll_rfkr_wum$_wke3m5g@ot9fh334k20b5tbx%$%x('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LOG_LEVEL = 'DEBUG'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # django otras
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    # apps del proyecto
    'common',
    'apirest',
    'cutreronte',
    'telegramapp',
    'sniffer',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cutreronte_v2.urls'

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

WSGI_APPLICATION = 'cutreronte_v2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'



# CELERY CONFIGURATION
# recommended settings: https://www.cloudamqp.com/docs/celery.html
CELERY_BROKER_POOL_LIMIT = 1  # Will decrease connection usage
CELERY_BROKER_HEARTBEAT = None  # We're using TCP keep-alive instead
CELERY_BROKER_CONNECTION_TIMEOUT = 30  # May require a long timeout due to Linux DNS timeouts etc
CELERY_RESULT_BACKEND = None  # AMQP is not recommended as result backend as it creates thousands of queues
CELERY_SEND_EVENTS = False  # Will not create celeryev.* queues
CELERY_EVENT_QUEUE_EXPIRES = 60  # Will delete all celeryev. queues without consumers after 1 minute.
CELERY_BROKER_URL = os.environ.get('CLOUDAMQP_URL', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_DEFAULT_QUEUE = 'priority.high'


# TELEGRAM
TELEGRAM_TOKEN = "612990444:AAHG8A7NdpuBgnPKFCMhK19CmXwKMxw4qEs"  # Sobreescribir en local_settings
TELEGRAM_GRUPO_LOG = 0
TELEGRAM_GRUPO_GENERAL = 0


SNIFFER_SERIE_PUERTO = "/dev/ttyUSB0"
SNIFFER_SERIE_BAUDRATE = 115200
SNIFFER_TIMEOUT_SENAL = 15 * 60  # segundos que tienen que pasar para dar un dispositivo por desconectado

try:
    from .local_settings import *
except ImportError:
    pass


LOGGING  = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, LOG_LEVEL.lower() + '.log'),
            'formatter': 'verbose',
        },
        'consola': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'consola'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}
