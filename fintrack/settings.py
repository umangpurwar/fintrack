"""
FinTrack Settings
-----------------
Environment-aware Django configuration for FinTrack v1.0.
Uses python-decouple to read from .env file in development
and from system environment variables in production (Render).

SRS References:
  - Section 7: Technical Requirements
  - NFR-SEC-01: HTTPS enforcement
  - NFR-SEC-03: Secrets as env vars
  - NFR-SEC-04: DEBUG=False in production
  - NFR-REL-02: External PostgreSQL
"""

from pathlib import Path
from decouple import config, Csv
import dj_database_url

# ─────────────────────────────────────────────────────────
# BASE PATHS
# ─────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR is the outer fintrack/ folder (where manage.py lives).
# Path(__file__) is this settings.py file.
# .parent.parent goes up two levels: fintrack/fintrack/settings.py → fintrack/fintrack/ → fintrack/


# ─────────────────────────────────────────────────────────
# SECURITY — READ FROM ENVIRONMENT
# ─────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')
# Reads SECRET_KEY from .env file. Raises an error if not set.
# This is intentional — the app should not start without a secret key.

DEBUG = config('DEBUG', default=False, cast=bool)
# Reads DEBUG from .env. Defaults to False (production-safe).
# In development .env, set DEBUG=True.

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())
# Reads comma-separated hostnames. Csv() splits the string into a Python list.
# Example: "127.0.0.1,localhost" becomes ['127.0.0.1', 'localhost']


# ─────────────────────────────────────────────────────────
# APPLICATION DEFINITION
# ─────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django's built-in apps:
    'django.contrib.admin',        # Admin panel at /admin/
    'django.contrib.auth',         # Authentication system (User, Group, Permission)
    'django.contrib.contenttypes', # Content type framework (required by admin and auth)
    'django.contrib.sessions',     # Session framework (for login state)
    'django.contrib.messages',     # Flash messages framework (success/error banners)
    'django.contrib.staticfiles',  # Static file management

    # Third-party apps:
    # (none in Module 0A)

    # Our project apps (to be added in future modules):
    # 'suppliers',
    # 'purchases',
    # 'reports',
    # 'credit',
    # 'pnl',
]


# ─────────────────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # SecurityMiddleware MUST be first. Handles HTTPS redirect, HSTS headers, etc.

    'whitenoise.middleware.WhiteNoiseMiddleware',
    # WhiteNoise MUST be second (right after SecurityMiddleware).
    # It intercepts requests for static files and serves them directly,
    # preventing them from passing through the rest of the middleware stack.

    'django.contrib.sessions.middleware.SessionMiddleware',
    # Manages session cookies — required for login/logout to work.

    'django.middleware.common.CommonMiddleware',
    # Handles URL normalization (trailing slashes), etc.

    'django.middleware.csrf.CsrfViewMiddleware',
    # CSRF protection — required by NFR-SEC-02. Validates CSRF tokens on POST requests.

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Associates the logged-in User object with every request (request.user).

    'django.contrib.messages.middleware.MessageMiddleware',
    # Required for Django's flash messages (success/error banners).

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Adds X-Frame-Options: DENY header to prevent clickjacking.
]


# ─────────────────────────────────────────────────────────
# URL CONFIGURATION
# ─────────────────────────────────────────────────────────
ROOT_URLCONF = 'fintrack.urls'
# Points to fintrack/urls.py as the root URL dispatcher.


# ─────────────────────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        # BASE_DIR / 'templates' = fintrack/templates/
        # This tells Django to look for templates in the top-level templates/ folder.
        # App-level templates (in app/templates/) are found via APP_DIRS=True below.

        'APP_DIRS': True,
        # When True, Django also searches for templates inside each installed app's
        # templates/ subfolder. This is how app-specific templates will be found
        # in future modules (e.g., suppliers/templates/suppliers/supplier_list.html).

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                # Adds 'debug' variable to template context.

                'django.template.context_processors.request',
                # Adds 'request' object to template context.
                # Required by Django's admin and auth views.

                'django.contrib.auth.context_processors.auth',
                # Adds 'user' and 'perms' to every template context.
                # This is how templates check {% if user.is_authenticated %}.

                'django.contrib.messages.context_processors.messages',
                # Adds 'messages' to template context for flash message display.
            ],
        },
    },
]


# ─────────────────────────────────────────────────────────
# WSGI APPLICATION
# ─────────────────────────────────────────────────────────
WSGI_APPLICATION = 'fintrack.wsgi.application'
# Points to the WSGI callable in fintrack/wsgi.py.
# Gunicorn uses this in production.


# ─────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        # conn_max_age=600: Keep database connections open for 600 seconds (10 minutes).
        # This is connection pooling — prevents opening a new DB connection on every request,
        # which is expensive. 600 seconds is a standard value for production apps.
    )
}
# dj_database_url.config() reads DATABASE_URL from environment and converts it to:
# {
#   'ENGINE': 'django.db.backends.postgresql',
#   'NAME': 'fintrack_db',
#   'USER': 'postgres',
#   'PASSWORD': 'yourpassword',
#   'HOST': 'localhost',
#   'PORT': '5432',
# }


# ─────────────────────────────────────────────────────────
# AUTHENTICATION
# ─────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # Prevents passwords too similar to username, email, or name.

    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    # Minimum 8 characters.

    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # Rejects passwords from a list of common passwords (e.g., "password123").

    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    # Prevents passwords that are entirely numeric.
]

LOGIN_URL = '/accounts/login/'
# Where unauthenticated users are redirected when they try to access a protected page.
# Django's built-in auth views are at /accounts/ by default.

LOGIN_REDIRECT_URL = '/'
# After a successful login, redirect to the home/dashboard page.

LOGOUT_REDIRECT_URL = '/accounts/login/'
# After logout, redirect to the login page.


# ─────────────────────────────────────────────────────────
# INTERNATIONALISATION
# ─────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
# FinTrack operates in India. All DateTimeField values will be in IST.
# The SRS specifies Indian financial year (April–March) and INR currency.

USE_I18N = True
USE_TZ = True
# USE_TZ=True stores datetimes as UTC in the database.
# Django converts to TIME_ZONE (IST) when displaying.
# This is correct behaviour — always store UTC, display local.


# ─────────────────────────────────────────────────────────
# STATIC FILES
# ─────────────────────────────────────────────────────────
STATIC_URL = '/static/'
# The URL prefix for static files. CSS loaded via 

STATIC_ROOT = BASE_DIR / 'staticfiles'
# Where 'python manage.py collectstatic' gathers all static files.
# WhiteNoise serves files from here in production.
# This directory is created by collectstatic — do NOT create it manually.

STATICFILES_DIRS = [
    BASE_DIR / 'static',
    # Your own static files are in fintrack/static/
    # collectstatic will copy them to staticfiles/ along with Django admin's static files.
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# WhiteNoise's storage backend. Does two things:
# 1. Compresses static files (gzip) for faster delivery.
# 2. Adds content-hash fingerprints to filenames (e.g., custom.abc123.css)
#    so browsers know to invalidate their cache when files change.


# ─────────────────────────────────────────────────────────
# DEFAULT PRIMARY KEY
# ─────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# All models that don't specify a primary key get an auto-incrementing BigInteger ID.
# BigAutoField supports up to 9.2 × 10^18 rows — sufficient for any foreseeable use.


# ─────────────────────────────────────────────────────────
# PRODUCTION SECURITY SETTINGS
# ─────────────────────────────────────────────────────────
if not DEBUG:
    # These settings are only active when DEBUG=False (production).
    # They would interfere with local development if always on.

    SECURE_SSL_REDIRECT = True
    # NFR-SEC-01: Redirect all HTTP requests to HTTPS.
    # Render provides HTTPS automatically — this enforces it at the Django level.

    SESSION_COOKIE_SECURE = True
    # Session cookie is only sent over HTTPS. Prevents session hijacking over HTTP.

    CSRF_COOKIE_SECURE = True
    # CSRF cookie is only sent over HTTPS.

    SECURE_HSTS_SECONDS = 31536000
    # HTTP Strict Transport Security. Tells browsers to only use HTTPS for this domain
    # for the next 31536000 seconds (1 year). Once set, browsers will refuse HTTP.

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # Apply HSTS to subdomains too.

    SECURE_HSTS_PRELOAD = True
    # Allows the domain to be submitted to browsers' HSTS preload list.

    SECURE_BROWSER_XSS_FILTER = True
    # Adds X-XSS-Protection header for older browsers.

    SECURE_CONTENT_TYPE_NOSNIFF = True
    # Prevents browsers from guessing content type — security against MIME sniffing attacks.
