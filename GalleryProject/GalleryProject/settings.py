from pathlib import Path
from dotenv import load_dotenv
import os
from decouple import config
from .env.app_Logic.KeyPass import SETTINGS_KEYS

#-------------------------------------------------------------------------------------------------------#
# dev env settings 
#-------------------------------------------------------------------------------------------------------#

BASE_DIR = Path(__file__).resolve().parent.parent
get_value = SETTINGS_KEYS

#-------------------------------------------------------------------------------------------------------#
# Project settings
#-------------------------------------------------------------------------------------------------------#

SECRET_KEY = get_value.DJANGO_KEY

DEBUG = get_value.DEBUG_STATE

ALLOWED_HOSTS = []

#-------------------------------------------------------------------------------------------------------#
# SMTP email setup
#-------------------------------------------------------------------------------------------------------#

EMAIL_HOST = get_value.EMAIL_HOSTING
EMAIL_HOST_USER = get_value.EMAIL_USER
EMAIL_HOST_PASSWORD = get_value.EMAIL_PASSWORD
EMAIL_PORT = get_value.EMAIL_PORT
EMAIL_USE_TLS = True
EMAIL_BACKEND = get_value.EMAIL_BACKEND_SMTP

#-------------------------------------------------------------------------------------------------------#
# Base Directory setup
#-------------------------------------------------------------------------------------------------------#

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'site_app',
    'gallery',
    'client',
    'bootstrap5',
    'ckeditor',
    'log_app',
    'storages',
    'user_system',
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

ROOT_URLCONF = 'GalleryProject.urls'

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

WSGI_APPLICATION = 'GalleryProject.wsgi.application'

#-------------------------------------------------------------------------------------------------------#
# Database and Autherization
#-------------------------------------------------------------------------------------------------------#

DATABASES = {
  'default': {
    'ENGINE': 'django_psdb_engine',
    'NAME': get_value.DB_NAME,
    'HOST': get_value.DB_HOST,
    'PORT': get_value.DB_PORT,
    'USER': get_value.DB_USER,
    'PASSWORD': get_value.DB_PASSWORD,
    'OPTIONS': {'ssl': {'ssl-ca': get_value.MYSQL_ATTR_SSL_CA}, 'charset': 'utf8mb4'}
  } 
}

#-------------------------------------------------------------------------------------------------------#
# Password validation
#-------------------------------------------------------------------------------------------------------#

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

#-------------------------------------------------------------------------------------------------------#
# Time-zone/Language  
#-------------------------------------------------------------------------------------------------------#

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

#-------------------------------------------------------------------------------------------------------#
# Directory and URLS 
#-------------------------------------------------------------------------------------------------------#

STATIC_URL = 'static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
