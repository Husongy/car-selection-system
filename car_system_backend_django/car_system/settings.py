"""
Django settings for car_system project.
新能源汽车智能选车系统
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-in-production-key-12345'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'simpleui',  # SimpleUI 必须放在 django.contrib.admin 之前
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 第三方应用
    'corsheaders',
    
    # 本地应用
    'apps.cars.apps.CarsConfig',
    'apps.users.apps.UsersConfig',
    'apps.analysis.apps.AnalysisConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'car_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'car_system.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'car_system'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'root'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3307'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS 配置
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# SimpleUI 配置
SIMPLEUI_CONFIG = {
    'system_keep': False,  # 不显示默认的 Django 系统配置
    'menu_display': ['汽车管理', '用户管理', '数据分析'],  # 菜单显示
    'dynamic': True,  # 动态菜单
    'menus': [
        {
            'name': '汽车管理',
            'icon': 'fas fa-car',
            'models': [
                {'name': '品牌管理', 'url': 'cars/brand/', 'icon': 'fa fa-copyright'},
                {'name': '车系管理', 'url': 'cars/carseries/', 'icon': 'fa fa-list'},
                {'name': '销量数据', 'url': 'cars/carsale/', 'icon': 'fa fa-chart-line'},
                {'name': '质量问题', 'url': 'cars/carissue/', 'icon': 'fa fa-exclamation-triangle'},
            ]
        },
    ]
}

SIMPLEUI_HOME_INFO = False  # 不显示首页信息
SIMPLEUI_ANALYSIS = False  # 不显示分析页面
SIMPLEUI_LOGO = 'https://avatars.githubusercontent.com/u/13655483'  # Logo
