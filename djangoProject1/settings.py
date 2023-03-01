"""
Django settings for djangoProject1 project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "QFZ3RmnQSZzDKrDNvWaXO9KGn9weWbJsTmSIX4ChABU"


# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'


ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    "allauth",  # new
    "allauth.account",  # new
    #ya user session kako bi izlogovao prethodnog usera
    'user_sessions',
    # my apps
    'slikeRadar.apps.SlikeradarConfig',
    # Local
    "accounts.apps.AccountsConfig",  # new
    # to o run code on a schedule 'django_q
    'django_q',
    #ya filtriranje na stranici koristim ovu app
    "django_filters",
    #widget za datum i vrijeme
    "bootstrap_datepicker_plus",
    #django app koja sprecava da se dva usera uloguju sa istim username i paswordom
    #potrebno je i MIDDLEWARE_CLASSES  definisati
   # 'preventconcurrentlogins',
    # bilt in django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # new
    # Third-party
    'django_cleanup.apps.CleanupConfig',
    "crispy_forms",  # new
    "crispy_bootstrap5",  # new

    "allauth.socialaccount",
    'allauth.socialaccount.providers.google',  # ... include the providers you want to enable

]
# MIDDLEWARE_CLASSES = {
#             #koristi da bi se sprecio login dva usera sa istim username i password
#             'preventconcurrentlogins.middleware.PreventConcurrentLoginsMiddleware',
#     }

MIDDLEWARE = [

    #kako bi se sprijecio Multiple Sessions for a User
    #"accounts.middleware.OneSessionPerUserMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
# kako bi se sprijecio Multiple Sessions for a User
    "accounts.middleware.SessionLimitMiddleware",

]

ROOT_URLCONF = "djangoProject1.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djangoProject1.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'PGO',
        'USER': 'root',
        'PASSWORD': 'PGOpass@23',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # new
STATIC_ROOT = BASE_DIR / "staticfiles"  # new
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"  # new
# folder u kojem se nalaze slike
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomUser"  # new

# django-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"  # new
CRISPY_TEMPLATE_PACK = "bootstrap5"  # new

# django-allauth config
LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT = "home"  # new
SITE_ID = 1
#SESSION_ENGINE = "django.contrib.sessions.backends.file"
AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",
    # "django.contrib.auth.backends.ModelBackend",


)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ACCOUNT_SESSION_REMEMBER = True  # new
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False  # new
ACCOUNT_USERNAME_REQUIRED = False  # new
ACCOUNT_AUTHENTICATION_METHOD = "username"  # new
ACCOUNT_EMAIL_REQUIRED = True  # new
ACCOUNT_UNIQUE_EMAIL = True  # new

# to o run code on a schedule 'django_q
# Configure your Q cluster
# More details https://django-q.readthedocs.io/en/latest/configure.html
Q_CLUSTER = {
    "name": "default",
    'timeout': 80,
    'retry': 85,
    'workers': 4,
    "orm": "default",  # Use Django's ORM + database for broker
}
