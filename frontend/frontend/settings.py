import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MODE = os.environ.get('MODE', 'local')

config_file = BASE_DIR.parent / os.environ.get('CONFIG_FILE', 'config.yaml')

with open(config_file, 'r') as file:
    config = yaml.safe_load(file)

env = config[MODE][BASE_DIR.name]

SECRET_KEY = env["django"].get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = bool(int(env["django"].get('DEBUG')))
DEBUG = True
ALLOWED_HOSTS = env["django"].get("ALLOWED_HOSTS").split(" ")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.authentication',
    'apps.errors',
    'apps.home',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# if DEBUG:
#     INSTALLED_APPS += ['whitenoise']
#     MIDDLEWARE.insert(0, 'whitenoise.middleware.WhiteNoiseMiddleware')
#     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'frontend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'frontend.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.authentication.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.authentication.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.authentication.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.authentication.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# STATIC_URL = '/static/audience-allocation/'
# STATIC_ROOT = BASE_DIR / 'static' / 'audience-allocation'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # куда collectstatic собирает файлы

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # путь к папке с дополнительными статическими файлами
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BACKEND_URL = env["backend"].get('BACKEND_URL')

ROLES_CHOICES = (
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('teacher', 'Преподаватель'),
)
ROLES = ['teacher', 'moderator', 'admin']

ROLE_MENU = {
    'teacher': [
        ('/auditoriums', 'Доступные аудитории'),
        ('/book', 'Забронировать'),
    ],
    'moderator': [
        ('/teachers', 'Преподаватели'),
    ],
    'admin': [
        ('/manage/auditoriums', 'Управление аудиториями'),
        ('/limits', 'Ограничения по бронированию'),
    ]
}


def permitted_roles(role):
    return ROLES[ROLES.index(role):]
