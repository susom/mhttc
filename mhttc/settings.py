"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuration environment
GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID")
TWITTER_USERNAME = os.environ.get("TWITTER_USERNAME")
INSTAGRAM_USERNAME = os.environ.get("INSTAGRAM_USERNAME")
FACEBOOK_USERNAME = os.environ.get("FACEBOOK_USERNAME")

# SendGrid and Help Contact Email
HELP_CONTACT_EMAIL = os.environ.get("HELP_CONTACT_EMAIL")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDGRID_SENDER_EMAIL = os.environ.get("SENDGRID_SENDER_EMAIL", HELP_CONTACT_EMAIL)

# Sending password reset emails
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587  # 25 or 587 (for unencrypted/TLS connections).
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = SENDGRID_SENDER_EMAIL

# You likely will need to set the domain name after it's been allocated
DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "http://127.0.0.1:8000")

SOCIAL_AUTH_LOGIN_REDIRECT_URL = DOMAIN_NAME

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Update the secret key to a value of your own before deploying the app.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if os.environ.get("GAE_APPLICATION") is not None and os.environ.get('GAE_SERVICE') == 'development':
    DEBUG = True

# Custom user model
AUTH_USER_MODEL = "users.User"

# SECURITY WARNING: App Engine's security features ensure that it is safe to
# have ALLOWED_HOSTS = ['*'] when the app is deployed. If you deploy a Django
# app not on App Engine, make sure to set an appropriate host here.
# See https://docs.djangoproject.com/en/2.1/ref/settings/
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "mhttc.apps.base",
    "mhttc.apps.main",
    "mhttc.apps.users",
    "django.contrib.admin",
    "import_export",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django_gravatar",
    "bootstrap4",
    "bootstrap_datepicker_plus",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mhttc.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "mhttc.apps.base.context_processors.domain_processor",
                "mhttc.apps.base.context_processors.social_processor",
            ],
        },
    },
]

TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG
WSGI_APPLICATION = "mhttc.wsgi.application"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Sentry for Monitoring

SENTRY_ID = os.environ.get("SENTRY_ID")
if SENTRY_ID is not None:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_ID,
        integrations=[DjangoIntegration()],
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# Install PyMySQL as mysqlclient/MySQLdb to use Django's mysqlclient adapter
# See https://docs.djangoproject.com/en/2.1/ref/databases/#mysql-db-api-drivers
# for more information
import pymysql  # noqa: 402

pymysql.version_info = (1, 4, 6, "final", 0)  # change mysqlclient version
pymysql.install_as_MySQLdb()

if os.getenv("MYSQL_HOST") is not None:
    # Running on production App Engine, connect to production database
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": os.environ.get("MYSQL_HOST"),
            "USER": os.environ.get("MYSQL_USER"),
            "PASSWORD": os.environ.get("MYSQL_PASSWORD"),
            "NAME": os.environ.get("MYSQL_DATABASE"),
            "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        }
    }

    # If we are on app engine, ensure https only
    if os.getenv("RUNNING_APP_ENGINE") == "yes":
        SECURE_SSL_REDIRECT = True
else:
    # Use sqlite when testing locally
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": os.environ.get("MYSQL_HOST"),
            "USER": os.environ.get("MYSQL_USER"),
            "PASSWORD": os.environ.get("MYSQL_PASSWORD"),
            "NAME": os.environ.get("MYSQL_DATABASE"),
            "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: 501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: 501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: 501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: 501
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = "static"
STATIC_URL = "/static/"

# Rate Limiting

VIEW_RATE_LIMIT = "100/1d"  # The rate limit for each view, django-ratelimit, "50 per day per ipaddress)
VIEW_RATE_LIMIT_BLOCK = (
    True  # Given that someone goes over, are they blocked for the period?
)

# On any admin or plugin login redirect to standard social-auth entry point for agreement to terms
LOGIN_REDIRECT_URL = "/login"

# CSP config
CSP_DEFAULT_SRC = ["'self'"]
CSP_SCRIPT_SRC = ["'self'", "'unsafe-inline'", "https://unpkg.com", "https://html2canvas.hertzen.com/",
                  "https://med.stanford.edu/", "https://code.jquery.com/", "https://cdn.datatables.net/",
                  "https://cdnjs.cloudflare.com/", "https://maxcdn.bootstrapcdn.com/", "https://cdn.jsdelivr.net/"]
CSP_STYLE_SRC = (
"'self'", "'unsafe-inline'", "fonts.googleapis.com", "https://cdn.datatables.net/", "https://cdnjs.cloudflare.com/",
"https://maxcdn.bootstrapcdn.com/", "http://code.jquery.com/", "https://cdn.jsdelivr.net/")
CSP_FONT_SRC = (
"'self'", "https://fonts.gstatic.com", "https://maxcdn.bootstrapcdn.com/", "http://maxcdn.bootstrapcdn.com/")
CSP_IMG_SRC = ("* 'self' data: https:")

CSP_CONNECT_SRC = ("'self'",)
CSP_MANIFEST_SRC = ("'self'",)
CSP_INCLUDE_NONCE_IN = ['script-src', 'style-src']

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

# HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 15768000
