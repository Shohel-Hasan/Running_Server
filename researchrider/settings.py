from pathlib import Path
import os
# import django_heroku
import dj_database_url
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
base = environ.Path(__file__) - 2
if os.path.exists(base(".env")):
    environ.Env.read_env(base(".env"))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--28_d-!+j*k@1we^1n6(s4$g%_dhsbo8eb8#3gw^f$w=76r+jv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
MODE = env.str('MODE', default='production')
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'storages',
    # django_cleanup
    'django_cleanup.apps.CleanupConfig',
    # sorl thumbnail
    'sorl.thumbnail',
    # rest framework
    'rest_framework',
    'rest_framework.authtoken',
    # apps
    "corsheaders",
    'user_app',
    'group_app',
    'course_app',
    'post_app',
    'social_app',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'researchrider.urls'

AUTH_USER_MODEL = 'user_app.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'researchrider.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# ------------------------- Database settings ---------------------

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql",
        'NAME':  "researchriderDb",
        'USER' : "researchriderDb",
        'PASSWORD' : "researchriderDb",
        'HOST' : "rrdb.ce7ck5x0fm1x.us-west-1.rds.amazonaws.com",
        'PORT' : 5432,
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': env('DB_ENGINE'),
#         'NAME':  env('DB_NAME'),
#         'USER' : env('DB_USER'),
#         'PASSWORD' : env('DB_PASSWORD'),
#         'HOST' : env('DB_HOST'),
#         'PORT' : env('DB_PORT'),
#     }
# }

# --------------------------------- Database Setting -----------------------

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000'
]

# -------------------------- Email settings -----------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'researchriderit@gmail.com'
EMAIL_HOST_PASSWORD = 'Bubt24685'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = env('EMAIL_HOST')
# EMAIL_USE_TLS = env('EMAIL_USE_TLS')
# EMAIL_PORT = env('EMAIL_PORT')
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# --------------------------- End of Email settings ------------------------

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


#STATIC_URL = '/static/'
#STATICFILES_DIRS = [BASE_DIR / 'static']
#STATIC_ROOT = BASE_DIR / 'staticfiles'
#MEDIA_URL = '/media/'
#MEDIA_ROOT = BASE_DIR / 'media'
#print("Media Root: ", MEDIA_ROOT)

# STATIC_URL = '/static/'
# MEDIA_URL = '/media/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]

# if MODE == 'local':
#     STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#     MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# elif MODE == 'production':  # below 3 line would be not use
#     STATIC_ROOT = '/home/' + env.str('USERNAME') + '/public_html/static'
#     MEDIA_ROOT = '/home/' + env.str('USERNAME') + '/public_html/media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
}

# heroku
# django_heroku.settings(locals())
# --------------------------- S3 file storage --------------------------
#DEFAULT_FILE_STORAGE="storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID="AKIAWTYPUUHPKER5U6IM"
AWS_SECRET_ACCESS_KEY="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"
AWS_STORAGE_BUCKET_NAME="researchrider"
#AWS_S3_FILE_OVERWRITE=False
AWS_DEFAULT_ACL=None
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
#AWS_LOCATION = 'media'
# s3 static settings
STATIC_LOCATION = 'static'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATICFILES_STORAGE = 'researchrider.storage_backends.StaticStorage'
#STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# s3 public media settings
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'researchrider.storage_backends.PublicMediaStorage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE')
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_FILE_OVERWRITE = env('AWS_S3_FILE_OVERWRITE')
# AWS_DEFAULT_ACL = env('AWS_DEFAULT_ACL')

# ---------------------------- End S3 Storage --------------------------


# HTTPS
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_BROWSER_XSS_FILTER = True
