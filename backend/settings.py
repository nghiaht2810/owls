"""
Django settings for backend project.
Optimized for Mini LMS Project (Django + Remix).
"""

from pathlib import Path
import os
import environ # Cần cài: pip install django-environ

# 1. Setup Environment Variables
# ------------------------------------------------------------------------------
env = environ.Env()
# Đọc file .env nếu có
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# 2. General Settings
# ------------------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')


# 3. Apps Definition
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

LOCAL_APPS = [
    'apps.courses',
    'apps.enrollments',
    'apps.users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Phải đặt trên cùng để handle request từ Remix
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# 4. Database
# ------------------------------------------------------------------------------
# Logic cũ của bạn quá dài. django-environ xử lý việc này chỉ với 1 dòng.
# Nó tự động parse DATABASE_URL (postgres://...) hoặc fallback về sqlite.
DATABASES = {
    'default': env.db('DATABASE_URL')
}


# 5. Password Validation
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# 6. Internationalization
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC' # Khuyến nghị giữ UTC cho Backend, Frontend sẽ tự convert sang giờ VN
USE_I18N = True
USE_TZ = True


# 7. Static & Media Files
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# 8. Django REST Framework & JWT
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

# Cấu hình JWT (Optional - Thêm vào để kiểm soát thời gian sống của token)
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Token sống 60 phút
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}


# 9. CORS Configuration (Kết nối với Remix)
# ------------------------------------------------------------------------------
# Thay vì allow all (nguy hiểm), chỉ cho phép Remix port
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')

# Nếu cần gửi Cookie/Auth headers qua CORS
CORS_ALLOW_CREDENTIALS = True