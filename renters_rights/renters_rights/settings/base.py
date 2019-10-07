"""
Django settings for renters' rights project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, default=None):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default:
            return default
        raise ImproperlyConfigured(f"Set the {var_name} environment variable")


def str_to_bool(value):
    str_value = str(value)
    true = str_value.lower() in ("yes", "true", "t", "1")
    false = str_value.lower() in ("no", "false", "f", "0")
    if true or false:
        return true or not false
    raise Exception("Bad string boolean value")


def str_to_int(value):
    return value if isinstance(value, int) else int(value)


SITE_NAME = get_env_variable("SITE_NAME", "Renters' Haven")
SITE_URL = get_env_variable("SITE_URL", "https://landlord/")
SITE_ID = 1

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "7a9+m*y!4!951^c1ocyzp)bs51b(2*vc_==qh3^s%yx-ie*!@#"

LOGIN_URL = "/auth/log-in/"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "localflavor",
    "modeltranslation",
    "maintenance_mode",
    "phonenumber_field",
    "units",
    "documents",
    "noauth",
    "active_link",
    "sass_processor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "maintenance_mode.middleware.MaintenanceModeMiddleware",
    "units.middleware.TurbolinksMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
]

ROOT_URLCONF = "renters_rights.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            # "loaders": [
            #     ("django.template.loaders.filesystem.Loader", ["templates"]),
            #     "django.template.loaders.app_directories.Loader",
            # ],
        },
        "APP_DIRS": True,
    }
]

WSGI_APPLICATION = "renters_rights.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "renters_rights",
        "USER": "postgres",
        "PASSWORD": "pass",
        "HOST": "db",
        "PORT": "5432",
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]


STATIC_URL = "/s/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOCALE_PATHS = [os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "locale"))]

# User registration
DEFAULT_FROM_EMAIL = get_env_variable("DEFAULT_FROM_EMAIL", "no-reply@renterhaven.com")
AUTH_USER_MODEL = "noauth.User"
NOAUTH_CODE_TTL_MINUTES = 10

# Smallest size will be used to generate a square thumbnail.
# Largest size will be used to resize original image.
# Sizes in-between will be used to generate thumbnails.
UNIT_IMAGE_SIZES = [200, 500, 1000]
UNIT_IMAGE_MAX_HEIGHT_AND_WIDTH = UNIT_IMAGE_SIZES[-1]
UNIT_IMAGE_MIN_HEIGHT_AND_WIDTH = UNIT_IMAGE_SIZES[0]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {"handlers": ["console"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"), "propagate": True},
        "units": {"handlers": ["console"], "level": os.getenv("LOG_LEVEL", "INFO")},
    },
}

PHONENUMBER_DB_FORMAT = "RFC3966"
PHONENUMBER_DEFAULT_REGION = "US"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"

gettext = lambda s: s
LANGUAGES = (("en", gettext("English")),)

# HTTP Basic auth. Username and password must both be set to have an effect.
# Good for test sites, pre-release, etc.
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME", "")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD", "")
if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
    MIDDLEWARE.insert(0, "lib.middleware.BasicAuthMiddleware")

MAX_THREAD_POOL_WORKERS = (
    str_to_int(os.getenv("MAX_THREAD_POOL_WORKERS", None)) if os.getenv("MAX_THREAD_POOL_WORKERS", None) else None
)
MAX_DOCUMENTS_PER_UNIT = os.getenv("MAX_DOCUMENTS_PER_UNIT", 5)
MAX_MOVE_IN_PICTURES_PER_UNIT = os.getenv("MAX_MOVE_IN_PICTURES_PER_UNIT", 12)
MAX_MOVE_OUT_PICTURES_PER_UNIT = os.getenv("MAX_MOVE_OUT_PICTURES_PER_UNIT", 12)

AWS_S3_ENDPOINT_URL = None
AWS_S3_CUSTOM_DOMAIN = None
AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID", "INVALID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY", "INVALID")
AWS_UPLOAD_BUCKET_NAME = get_env_variable("AWS_UPLOAD_BUCKET_NAME", "renters-rights-uploads-test")
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME", "renters-rights-test")

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
