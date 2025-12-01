"""
Django settings for votaciones project (Render Production Ready)
"""

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 SECRET KEY desde variable de entorno
SECRET_KEY = os.getenv("SECRET_KEY", "insecure-key")

# 🚫 DEBUG DESACTIVADO EN PRODUCCIÓN
DEBUG = os.getenv("DEBUG", "False") == "True"

# 🌍 Host permitido (Render)
ALLOWED_HOSTS = ['.onrender.com', 'localhost']

# -------------------- APPS --------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "usuarios",
]

# -------------------- MIDDLEWARE --------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Para servir estáticos en Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "votaciones.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "votaciones.wsgi.application"

# -------------------- DATABASE --------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# -------------------- PASSWORD VALIDATION --------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------- INTERNATIONALIZATION --------------------
LANGUAGE_CODE = "es-pe"
TIME_ZONE = "America/Lima"
USE_I18N = True
USE_TZ = True

# -------------------- STATIC FILES --------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_DIRS = [
    BASE_DIR / "usuarios" / "static",
]

# -------------------- LOGIN --------------------
LOGIN_URL = '/usuarios/login/'
LOGIN_REDIRECT_URL = '/usuarios/votar/'
LOGOUT_REDIRECT_URL = '/usuarios/login/'

# -------------------- DEFAULT PRIMARY KEY --------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
