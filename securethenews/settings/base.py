"""
Django settings for securethenews project.

Generated by 'django-admin startproject' using Django 1.9.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from __future__ import absolute_import, unicode_literals

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

DEBUG = False

# Application definition

INSTALLED_APPS = [
    'home',
    'search',
    'sites',
    'blog',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.contrib.legacy.richtext',
    'wagtail.core',

    'wagtail.contrib.modeladmin',
    'wagtail.contrib.table_block',

    'wagtailautocomplete',
    'wagtailmenus',
    'webpack_loader',
    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_filters',
    'crispy_forms',
    'rest_framework',
    'corsheaders',
    'django_logging',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

# Must be directly after SecurityMiddleware
if os.environ.get('DJANGO_WHITENOISE'):
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

MIDDLEWARE.extend([
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'django_logging.middleware.DjangoLoggingMiddleware',

    # Middleware for content security policy
    'csp.middleware.CSPMiddleware',
])


# Django HTTP settings

# Anyone can use the API via CORS
CORS_ORIGIN_ALLOW_ALL = True

# API is read-only
CORS_ALLOW_METHODS = ('GET', 'HEAD', 'OPTIONS')

# Set X-XSS-Protection
SECURE_BROWSER_XSS_FILTER = True

# Set X-Content-Type-Options
SECURE_CONTENT_TYPE_NOSNIFF = True

# Rather than sending a header, this says to trust this request header (in
# prod we are behind nginx, which sets it)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Make the deployment's onion service name available to templates
ONION_HOSTNAME = os.environ.get('DJANGO_ONION_HOSTNAME')


ROOT_URLCONF = 'securethenews.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtailmenus.context_processors.wagtailmenus',
                'django_settings_export.settings_export',
            ],
        },
    },
]

WSGI_APPLICATION = 'securethenews.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

if 'DJANGO_DB_HOST' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DJANGO_DB_NAME', 'stn'),
            'USER': os.environ['DJANGO_DB_USER'],
            'PASSWORD': os.environ['DJANGO_DB_PASSWORD'],
            'HOST': os.environ['DJANGO_DB_HOST'],
            'PORT': os.environ['DJANGO_DB_PORT']
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'stn-build.sqlite3'),
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
    os.path.join(BASE_DIR, 'client', 'build'),
]

STATIC_ROOT = os.environ.get(
    'DJANGO_STATIC_ROOT', os.path.join(BASE_DIR, 'static'))
STATIC_URL = '/static/'

MEDIA_ROOT = os.environ.get(
    'DJANGO_MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))
MEDIA_URL = '/media/'


# Disable analytics by default
ANALYTICS_ENABLED = False

# Export analytics settings for use in site templates
SETTINGS_EXPORT = [
    'ANALYTICS_ENABLED',
]
# Prevent template variable name collision with wagtail settings
SETTINGS_EXPORT_VARIABLE_NAME = 'django_settings'


# Wagtail settings

WAGTAIL_SITE_NAME = "securethenews"


# Base URL to use when referring to full URLs within the Wagtail -
# admin backend e.g. in notification emails. Don't include
# '/admin' or a trailing slash
BASE_URL = 'https://securethe.news'


# API framework settings, relevant only for /api
REST_FRAMEWORK = {
    # For any query, users can set both limit and offset.
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    # A page has 100 results by default, but there's no upper limit.
    'PAGE_SIZE': 100,
}

# Shiny forms for the web view of the API
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django-webpack configuration
WEBPACK_LOADER = {  # noqa: W605
    'DEFAULT': {
        'CACHE': False,
        'BUNDLE_DIR_NAME': '/',  # must end with slash
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}


# Django test xml output
#

if os.environ.get('DJANGO_XMLTEST_OUTPUT', 'no').lower() in ['yes', 'true']:
    TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
    TEST_OUTPUT_DIR = "/django-logs"
    TEST_OUTPUT_FILE_NAME = "app-tests.xml"
    TEST_OUTPUT_DESCRIPTIONS = True
    TEST_OUTPUT_VERBOSE = 2

# Content Security Policy
# script:
# unsafe-eval for client/build/build.js
# unsafe-inline for admin
# style:
# unsafe-inline needed for wagtail admin inline styles
# #2 and #3 hashes needed for inline style for modernizr on admin page
# #4 needed for wagtail admin
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-eval'",
    "'unsafe-inline'",
    "https://analytics.freedom.press",
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
)
CSP_FRAME_SRC = ("'self'",)
CSP_CONNECT_SRC = (
    "'self'",
    "https://analytics.freedom.press",
)

# This will be used to evaluate Google Storage media support in staging
GS_CUSTOM_ENDPOINT = os.environ.get(
    "GS_CUSTOM_ENDPOINT",
    "https://media.securethe.news"
)

# Need to be lists for now so that CSP configuration can add to them.
# This should be reverted after testing.
CSP_IMG_SRC = (
    "'self'",
    "analytics.freedom.press",
    GS_CUSTOM_ENDPOINT,
)
CSP_OBJECT_SRC = (
    "'self'",
    GS_CUSTOM_ENDPOINT,
)
CSP_MEDIA_SRC = (
    "'self'",
    GS_CUSTOM_ENDPOINT,
)

# Report URI must be a string, not a tuple.
CSP_REPORT_URI = os.environ.get(
    'DJANGO_CSP_REPORT_URI',
    'https://freedomofpress.report-uri.com/r/d/csp/enforce'
)


# Logging
#
# Logs are now always JSON. Normally, they go to stdout. To override this for
# development or legacy deploys, set DJANGO_LOG_DIR in the environment.

log_level = os.environ.get("DJANGO_LOG_LEVEL", "info").upper()
log_format = os.environ.get("DJANGO_LOG_FORMAT", "json")
log_stdout = True
log_handler = {
    "formatter": log_format,
    "class": "logging.StreamHandler",
    "stream": sys.stdout,
    "level": log_level,
}

log_dir = os.environ.get("DJANGO_LOG_DIR")
if log_dir:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_stdout = False
    log_handler = {
        "formatter": log_format,
        "class": "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(log_dir, "django-other.log"),
        "backupCount": 5,
        "maxBytes": 10000000,
        "level": log_level,
    }

DJANGO_LOGGING = {
    "LOG_LEVEL": log_level,
    "CONSOLE_LOG": log_stdout,
    "INDENT_CONSOLE_LOG": 0,
    "DISABLE_EXISTING_LOGGERS": True,
    "PROPOGATE": False,
    "SQL_LOG": False,
    "ENCODING": "utf-8",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "normal": log_handler,
        "null": {"class": "logging.NullHandler"},
    },
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
        },
        "plain": {
            "format": "%(asctime)s %(levelname)s %(name)s "
            "%(module)s %(message)s",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["normal"], "propagate": True,
        },
        "django.template": {
            "handlers": ["normal"], "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["normal"], "propagate": False,
        },
        "django.security": {
            "handlers": ["normal"], "propagate": False,
        },
        # These are already handled by the django json logging library
        "django.request": {
            "handlers": ["null"],
            "propagate": False,
        },
        # Log entries from runserver
        "django.server": {
            "handlers": ["null"], "propagate": False,
        },
        # Catchall
        "": {
            "handlers": ["normal"], "propagate": False,
        },
    },
}
