# Django settings for egosite project.
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



DEBUG = True
#TEMPLATE_DEBUG = DEBUG

# root path for the site
ROOT = os.path.dirname(os.path.abspath(__file__))
#SETTINGS_PATH = '/webapps/netwrkr/networker/egonet'

ADMINS = (
    ('Andrea Cavicchini', 'acavicchini@iese.edu'),
)

MANAGERS = ADMINS

EMAIL_HOST = 'smtp.webfaction.com'

EMAIL_HOST_USER = 'networker'

EMAIL_HOST_PASSWORD = 'Embedded'

SERVER_EMAIL = 'no_reply@networker.webfactional.com'

DEFAULT_FROM_EMAIL = 'no_reply@networker.webfactional.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2','mysql','sqlite3' or 'oracle'
        'NAME': 'egodb',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'egodb',
        'PASSWORD': 'lkj2ihvigayv2xwp',
        'HOST': 'app-329e8191-6edd-4f3b-a4bb-d938aca9edcb-do-user-845859-0.b.db.ondigitalocean.com',
        # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '25060',                      # Set to empty string for default.
    }
}



# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['127.0.0.1',
                 'egosite-srfaq.ondigitalocean.app']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Andorra'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'es-es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'
#MEDIA_URL = '/webapps/netwrkr/networker/media'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = os.path.join(ROOT, os.pardir, "static")
#STATIC_ROOT = '/webapps/netwrkr/networker/static'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# Extra places for collectstatic to find static files.


# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&h0g$#^7%!rj0$==3xjx9hx24!(@o5tbjq%9la!fdvrfhm@t28'

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
#    'admin_tools.template_loaders.Loader'
#)

#TEMPLATE_DIRS = (
#    '/webapps/netwrkr/networker/egonet/templates',
# )

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'egosite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'egosite.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/webapps/netwrkr/networker/static'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'debug' : True
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'egonet',
    'bootstrap3',
)

##
## Session stuff
##
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Default settings
BOOTSTRAP3 = {
    "error_css_class": "bootstrap3-error",
    "required_css_class": "bootstrap3-required",
    "javascript_in_head": True,
}


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
