"""
Django settings for linkpearl project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '672z)yzg3q+l)yd=1ja6t)g6%=69077sg8@kmkc0^%@v=)-k)@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'linkpearl',
    'linkpearl_lodestone',
    'debug_toolbar',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'linkpearl.urls'

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

WSGI_APPLICATION = 'linkpearl.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'linkpearl',
        'HOST': '10.10.10.10',
        'USER': 'linkpearl',
        'PASSWORD': 'linkpearl',
    }
}


# Caches
# https://docs.djangoproject.com/en/1.9/ref/settings/#caches

CACHES = {
    'default': {
        'BACKEND': 'caching.backends.memcached.PyLibMCCache',
        'LOCATION': '10.10.10.10',
        'KEY_PREFIX': 'linkpearl:',
    },
}

CACHE_COUNT_TIMEOUT = 60

CACHE_MACHINE_USE_REDIS = True

REDIS_BACKEND = 'redis://10.10.10.10:6379'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'


# Django-Celery integration (task autodetection, etc)
# https://pypi.python.org/pypi/django-celery

import djcelery
djcelery.setup_loader()

CELERY_RESULT_BACKEND='redis://10.10.10.10/0'

CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

BROKER_URL = 'amqp://linkpearl:linkpearl@10.10.10.10:5672//'


# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.org/en/1.4/index.html

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True,
    'SHOW_TOOLBAR_CALLBACK': 'linkpearl.settings._show_toolbar_callback',
}

def _show_toolbar_callback(request):
    return DEBUG and not request.is_ajax()
