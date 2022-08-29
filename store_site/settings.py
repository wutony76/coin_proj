from __future__ import print_function
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print('BASE_DIR', BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kxw67qq=6%048a4lrajg&r*ac@osb!-%e5#%!c^-c)5r=jn&h5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store_site',
    #'test_store',
    #'debug_site',
    #'siya',
    #'dipay',
]

MIDDLEWARE_CLASSES = [
    #'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'store_site.urls'
#ROOT_URLCONF = 'test_store.urls'
#ROOT_URLCONF = 'debug_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'store_site.wsgi.application'
#WSGI_APPLICATION = 'debug_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
from fcworks.conf import settings as _settings
#from fatcat.conf import settings as _settings

_db_ctx = {
  'ENGINE': 'django.db.backends.mysql',
  'NAME': 'pays_ahui',
  'USER': 'root',
  'PASSWORD': '&4RFV5tgb&',
  'HOST': '17.0.0.153',
  'PORT': 3306,
}
_db_ctx.update(_settings.COIN_MYSQL_DATABASE)


DATABASES = {
  'default': _db_ctx,
  #'default': {
  #  'ENGINE': 'django.db.backends.sqlite3',
    #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  #}
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")


SESSION_COOKIE_NAME = "fire_coin_sessid"
SESSION_PREFIX = "fire_coin_site"
SESSION_ENGINE = "store_site.sessions"


