"""
Django settings for sim_dashboard project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
	os.path.join(BASE_DIR, 'templates'),
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#i88gs=z(5ut&t6bz$&mvh-pd8q1@y%37+36nk+y%v!c*5s-)d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'result_manager',
    'series_manager',
    'result_viewer',
    'analyzer',
    'main',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sim_dashboard.urls'

WSGI_APPLICATION = 'sim_dashboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sim_ds',
        'USER': 'root',
        'PASSWORD': 'svn123',
        'HOST': '',
        'PORT': '',
        
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'utf-8'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        'simple': {
            'format': '%(levelname)s %(message)s'
            },
        'verysimple': {
            'format': '%(message)s'
            },
        },
    'filters': {
        },
    'handlers': {
        'to_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/application.log',
            'formatter': 'verbose',
            },
        'to_ctrl_file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'log/ctrl.log',
                'formatter': 'verysimple',
                },
        },    
    'loggers': {
        'application': {
            'handlers': ['to_file'],
            'level': 'DEBUG',
            'propagate': True,
            },
        'raw': {
            'handlers': ['to_ctrl_file'],
            'level': 'DEBUG',
            'propagate': True,
            },
        }
    }


LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = "/"

## Django-Celery
BROKER_URL="amqp://guest:guest@172.16.51.11:5672//"
#BROKER_HOST = "172.16.51.11"
#BROKER_PORT = 5672
#BROKER_USER = "guest"
#BROKER_PASSWORD = "guest"
#BROKER_VHOST = "/"
CELERY_RESULT_BACKEND = "amqp"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
