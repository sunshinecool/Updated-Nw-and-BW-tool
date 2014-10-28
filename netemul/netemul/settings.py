"""
Django settings for netemul project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nd8^79m(@eo@+8i9jyfklvqx1c$+90!8$#1=mg76y(n3c!f!n)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

MEDIA_ROOT = BASE_DIR+'/media/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'netemapp',
    'monitor',
    'app',
#    'django_socketio',
#    'highcharts',
    'chartit',
#    'googlecharts',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'netemul.urls'

WSGI_APPLICATION = 'netemul.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'netemul_db',
	'USER':'root',
	'PASSWORD':'123',
	'HOST':'',
	'PORT':'',
    }
}
TEMPLATE_DIRS = (
        BASE_DIR + '/static/'
)
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sree.leela92@gmail.com'
EMAIL_HOST_PASSWORD = '1992sreeleela1992'
 
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
APPEND_SLASH=False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = (
    BASE_DIR + '/static/',
)
LOGGING = {
            'version': 1,
                'disable_existing_loggers': False,
                    'filters': {
                                'require_debug_false': {
                                                '()': 'django.utils.log.RequireDebugFalse'
                                                        }
                                    },
                        'handlers': {
                                    'mail_admins': {
                                                    'level': 'ERROR',
                                                                'filters': ['require_debug_false'],
                                                                            'class': 'django.utils.log.AdminEmailHandler'
                                                                                    }
                                        },
                            'loggers': {
                                        'django.request': {
                                                        'handlers': ['mail_admins'],
                                                                    'level': 'ERROR',
                                                                                'propagate': True,
                                                                                        },
                                            }
                            }

