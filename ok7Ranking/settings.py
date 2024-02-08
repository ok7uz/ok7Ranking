import os
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-^ush_f&!nk3q$q=ld3_e42bj^iamon3v_2x2vcr79yy#7m4(p+'
 
debug = os.environ.get('DEBUG', 'True')
DEBUG = debug == 'True'
ALLOWED_HOSTS = ['*'] if DEBUG else ['127.0.0.1', 'ok7-rankings-91ee2cd70e74.herokuapp.com']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'ranking.apps.RankingConfig',
]

MIDDLEWARE = [
    'ok7Ranking.middleware.NoWWWRedirectMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
]

ROOT_URLCONF = 'ok7Ranking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ok7Ranking.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = urlparse(os.environ.get('DATABASE_URL'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_URL.path[1:],
        'USER': DATABASE_URL.username,
        'PASSWORD': DATABASE_URL.password,
        'HOST': DATABASE_URL.hostname,
        'PORT': DATABASE_URL.port,
         
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'staticfiles']
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
