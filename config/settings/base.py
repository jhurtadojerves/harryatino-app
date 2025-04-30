"""Base settings to build other settings files upon."""

import os
from pathlib import Path

from environs import Env

env = Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "apps"

# Base
DEBUG = env.bool("DJANGO_DEBUG", False)

# Language and timezone
TIME_ZONE = "America/Guayaquil"
LANGUAGE_CODE = "es-EC"

USE_I18N = True
USE_L10N = True
USE_TZ = True

# DATABASES
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", "app"),
        "HOST": os.getenv("DATABASE_HOST", "db"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
        "USER": os.getenv("DATABASE_USER", "root"),
        "PASSWORD": os.getenv("DATABASE_PASS", "root"),
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLs
ROOT_URLCONF = "config.urls"

# WSGI
WSGI_APPLICATION = "config.wsgi.application"

# Users & Authentication
AUTH_USER_MODEL = "authentication.User"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Apps
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.humanize",
    "django.contrib.postgres",
]

THIRD_PARTY_APPS = [
    "import_export",
    "superadmin",
    "ckeditor",
    "tracing",
    "django_select2",
    "mathfilters",
    "rest_framework",
]

LOCAL_APPS = [
    "apps.announcements",
    "apps.authentication",
    "apps.boxrooms",
    "apps.dices",
    "apps.dynamicforms",
    "apps.ecommerce",
    "apps.insoles",
    "apps.management",
    "apps.members",
    "apps.menu",
    "apps.pages",
    "apps.payments",
    "apps.products",
    "apps.profiles",
    "apps.properties",
    "apps.sales",
    "apps.utils",
    "apps.workflows",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Passwords
"""PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]"""
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Middlewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "tracing.middleware.TracingMiddleware",
    "config.middleware.GlobalRequestMiddleware",
]

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Media
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Select2
SELECT2_CSS = "vendors/select2/select2.min.css"
SELECT2_JS = "vendors/select2/select2.full.min.js"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.menu",
            ],
        },
    },
]

# Security
# SESSION_COOKIE_HTTPONLY = True
# CSRF_COOKIE_HTTPONLY = True
# SECURE_BROWSER_XSS_FILTER = True
# X_FRAME_OPTIONS = 'DENY'


# Admin
ADMIN_URL = "admin/"
ADMINS = [
    ("""Julio Hurtado""", "juliens@outlook.com"),
]
MANAGERS = ADMINS

# Hydra
BREADCRUMB_HOME_TEXT = "Inicio"
BREADCRUMB_CREATE_TEXT = "Crear"
BREADCRUMB_UPDATE_TEXT = "Editar"
BREADCRUMB_DETAIL_TEXT = ""
BREADCRUMB_DELETE_TEXT = "Eliminar"

BOOLEAN_YES = "Sí"
BOOLEAN_NO = "No"

TEMPLATE_WIDGETS = {
    "checkbox": "widgets/checkboxinput.html",
    "clearablefile": "widgets/fileinput.html",
    "date": "widgets/dateinput.html",
    "radioselect": "widgets/radioinput.html",
    "select": "widgets/selectinput.html",
    "datetime": "widgets/textinput.html",
    "email": "widgets/textinput.html",
    "select2": "widgets/textinput.html",
    "modelselect2": "widgets/textinput.html",
    "modelselect2multiple": "widgets/textinput.html",
    "number": "widgets/textinput.html",
    "password": "widgets/textinput.html",
    "text": "widgets/textinput.html",
    "lazyselect": "widgets/textinput.html",
    "datetime": "widgets/textinput.html",
    "RichTextUploadingField": "widgets/textinput.html",
    "selectmultiple": "widgets/textinput.html",
    "ckeditoruploading": "widgets/textinput.html",
    "ckeditor_upload": "widgets/textinput.html",
    "textarea": "widgets/textinput.html",
    "ckeditor": "widgets/textarea.html",
    "checkboxselectmultiple": "widgets/textinput.html",
    "time": "widgets/textinput.html",
    "modelselect2tag": "widgets/textinput.html",
    "url": "widgets/textinput.html",
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono-lisa",
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
        "toolbar_Full": [
            ["JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock"],
            [
                "Styles",
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                "Undo",
                "Redo",
            ],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Flash", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
            ["Source"],
        ],
        "toolbar": "Full",
        "height": 500,
        "width": 1400,
        "removePlugins": "autogrow",
    }
}
TEMPLATE_WIDGETS_DETAIL = {
    "default": "detail_widgets/textinput.html",
    "DateTimeField": "detail_widgets/textinput.html",
    "CharField": "detail_widgets/textinput.html",
    "DateField": "detail_widgets/dateinput.html",
    "BooleanField": "detail_widgets/booleantinput.html",
    "URLField": "detail_widgets/urlinput.html",
    "TextField": "detail_widgets/textarea.html",
    "ForeignKey": "detail_widgets/foreignkey.html",
    "OneToOneField": "detail_widgets/foreignkey.html",
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ]
}

SITE_URL = env.url("SITE_URL", "http://localhost:8000")
TOPIC_QUESTIONS = env.int("TOPIC_QUESTIONS", 106688)

MAGIC_MALL_TOPIC = env.int("MAGIC_MALL_TOPIC")
CHECKOUT_COOLDOWN_HOURS = env.int("CHECKOUT_COOLDOWN_HOURS", 12)
MOCK_CREATE_POST = False
CACHE_TTL = env.int("CACHE_TTL", 60 * 15)
