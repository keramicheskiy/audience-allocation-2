import os
from pathlib import Path

import pytz
import yaml
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

MODE = os.environ.get('MODE', 'local')

config_file = os.environ.get('CONFIG_FILE')

with open(config_file, 'r') as file:
    config = yaml.safe_load(file)

env = config[MODE][BASE_DIR.name]
db = config["db"][env["storage"]["type"]]

SECRET_KEY = env["django"].get('SECRET_KEY')

DEBUG = bool(int(env["django"].get('DEBUG')))
ALLOWED_HOSTS = env["django"].get("ALLOWED_HOSTS").split(" ")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'celery',
    'apps.authentication',
    'apps.auditoriums',
    'apps.equipments',
    'apps.lectures',
    'apps.my',
    'apps.role_approvance_requests',
    'apps.users',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates", ],
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

WSGI_APPLICATION = 'backend.wsgi.application'

DB_ENGINE = db.get('ENGINE')

if DB_ENGINE == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': db.get('NAME', 'postgres'),
            'USER': db.get('USER', 'postgres'),
            'PASSWORD': db.get('PASSWORD', 'postgres'),
            'HOST': db.get('HOST', 'localhost'),  # название контейнера для базы данных в docker-compose
            'PORT': db.get('PORT', '5432'),
        }
    }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

time_zone = pytz.timezone(env["django"].get('TIME_ZONE', "Europe/Moscow"))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.CustomUser'

# Celery и Redis
CELERY_BROKER_URL = env["celery"].get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = env["celery"].get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

# Почта
sender_email = env["email"].get('EMAIL')
email_password = env["email"].get('PASSWORD')
smtp_server = env["email"].get('SERVER')
smtp_port = env["email"].get('PORT')

# Corsheaders
CORS_ALLOWED_ORIGINS = [
    "http://frontend:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

ROLES_CHOICES = (
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('teacher', 'Преподаватель')
)

ROLES = ["teacher", "moderator", "admin"]


def permitted_roles(role):
    return ROLES[ROLES.index(role):]

TELEGRAM_BOT_TOKEN = env["telegram"].get('TOKEN')
