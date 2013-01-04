# -*- coding: utf-8 -*-
# Django settings for kolstat project.

import os, sys
import socket
import datetime

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Karol Farbiś', 'kpchwk@gmail.com'),
     ('Maciej Kacprzak', 'paramaciej@gmail.com'),
)

INSTALL_DIR = os.path.split(os.path.realpath(__file__))[0]
CACHE_DIR = os.path.join(INSTALL_DIR, 'cache')

HOST = socket.gethostbyaddr(socket.gethostname())[0]
DEPLOY = (HOST == 'kkjudge')

MANAGERS = ADMINS

if DEPLOY:
	DATABASES = {
   	 'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kolstat',
        'USER': 'kolstat',
 	   }
	}
	DEBUG = False
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': INSTALL_DIR + '/db/db.db',
		}
	}

TIME_ZONE = 'Europe/Warsaw'

LANGUAGE_CODE = 'pl'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = INSTALL_DIR + '/media'

MEDIA_URL = '/media/'

STATIC_ROOT = INSTALL_DIR + '/static'

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
	'dajaxice.finders.DajaxiceFinder',
)

SECRET_KEY = '8pj55gxjsst8&_$t_eur%%c$5x0#jdky9)ijelde@9v+&!d4bo'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'kolstat.urls'

TEMPLATE_DIRS = (
		INSTALL_DIR + '/templates/',
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
	'dajaxice',
	'kolstat.kolstatapp',
	'social_auth',
] 

if DEBUG:
	INSTALLED_APPS.append('debug_toolbar')
	MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
	INTERNAL_IPS = ('127.0.0.1',)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
		'stderr': {
            'class': 'logging.StreamHandler',
			'stream': sys.stderr,
			'level': 'DEBUG'
		},
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
		'dajaxice': {
            'handlers': ['stderr'],
				
		},
    }
}

DAJAXICE_MEDIA_PREFIX = "ajax"

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
		"django.core.context_processors.debug",
		"django.core.context_processors.i18n",
		"django.core.context_processors.media",
		"django.core.context_processors.static",
		"django.core.context_processors.request",
		"django.contrib.messages.context_processors.messages")

AUTHENTICATION_BACKENDS = (
			"social_auth.backends.facebook.FacebookBackend",
			"social_auth.backends.google.GoogleOAuth2Backend",
			"django.contrib.auth.backends.ModelBackend",
		)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/logged/'
LOGIN_ERROR_URL = '/accounts/login/error/'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

GOOGLE_OAUTH2_CLIENT_ID = '308170056415.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = '0Bo1vdwOympxtcEYdJvujISW'

TIMETABLE_START = datetime.date(2012,12,9)
TIMETABLE_END = datetime.date(2013,12,7)
TIMETABLE_YEAR = 2013
