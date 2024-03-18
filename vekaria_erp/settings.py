"""
Django settings for vekaria_erp project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@$t&uqomqqh^n!fp1$$vu0)@pt%zv&*q-1@2(iwx8_2bdqz81$'



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.15','103.21.160.164','localhost','0.0.0.0','*','http://vekaria-erp.prismtechs.in']
PRODUCTION=True
# Fontend URL:
HOST_URL='http://103.21.160.164:3000'
LOCALHOST='http://15.2.2.15:3000'

# email config 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'dev2.prismtechs@gmail.com'
EMAIL_HOST_PASSWORD = 'lbhvszdhkkgzjlgz'
EMAIL_FROM='dev2.prismtechs@gmail.com'

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authuser',
    'inventory_and_stores',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
   'channels',
     'channels_redis',
    'supply_chain',
    'notification',
    'masterdata',
    'sales',
    'qc_reports'
     
] 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'vekaria_erp.urls'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates'),],
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
# WSGI_APPLICATION = 'vekaria_erp.wsgi.application'
ASGI_APPLICATION = 'vekaria_erp.asgi.application'
import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'app': {
            'format': '%(asctime)s [%(levelname)-8s] (%(module)s.%(funcName)s) %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'app',
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': './log/django_server_errors.log',
            'formatter': 'app',
        },
        'file_warnings': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': './log/django_server_warnings.log',
            'formatter': 'app',
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './log/django.log',
            'formatter': 'app',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_errors', 'file_warnings', 'file_info'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Configure logging
logging.config.dictConfig(LOGGING)




# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "root": {"level": "INFO", "handlers": ["file"]},
#     "handlers": {
#         "file": {
#             "level": "INFO",
#             "class": "logging.FileHandler",
#             "filename": "/var/log/django.log",
#             "formatter": "app",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": "INFO",
#             "propagate": True
#         },
#     },
#     "formatters": {
#         "app": {
#             "format": (
#                 u"%(asctime)s [%(levelname)-8s] "
#                 "(%(module)s.%(funcName)s) %(message)s"
#             ),
#             "datefmt": "%Y-%m-%d %H:%M:%S",
#         },
#     },
# }

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases



# DATABASES = {
  
#       'default': {
# 'ENGINE': 'mssql',
# 'NAME': 'vekaria_erp_1.1_v',
# 'USER': 'Admin',
# 'PASSWORD':'Hello@123',
# 'HOST':'192.168.1.22',
# 'PORT':'1440',
# 'OPTIONS': {
#     'driver':'ODBC Driver 17 for SQL Server'
# }
#   }
    
# }
# DATABASES = {
  
# 'default': {
# 'ENGINE': 'mssql',
# 'NAME': 'vekaria_v1.2',
# 'USER': 'Admin',
# 'PASSWORD':'BrainisemptyPlease give me coffe@2024',
# 'HOST':'15.2.2.18',
# 'PORT':'5890',
# 'OPTIONS': {
#     'driver':'ODBC Driver 17 for SQL Server'
# }
#   }
    
# }

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'vekaria_erp_1.1_v',
        'HOST': '15.2.2.18,5890',  # Use double backslashes for the backslash in the server name
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'MARS_Connection': True,
            'Trusted_Connection': 'yes',  # Use Windows Authentication
        },
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': 'vekaria_erp_1.1_v',
#         'HOST': '192.168.1.21,4550',  # Use double backslashes for the backslash in the server name
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#             'MARS_Connection': True,
#             'Trusted_Connection': 'yes',  # Use Windows Authentication
#         },
#     }
# }


REST_FRAMEWORK = {
   
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
   
}

CORS_ORIGIN_ALLOW_ALL = True  

# CORS_ALLOWED_ORIGINS = [  
# 'http://localhost:3000','http://192.168.1.9:3000','http://192.168.1.21:3000'
# ]  

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
# if not DEBUG:
MEDIA_URL = '/media/'
# MEDIA_URL = 'http://localhost:5004/media/'
    # MEDIA_URL = 'http://103.21.160.164:5000/media/'
# else:
#     MEDIA_URL = '/media/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PASSWORD_RESET_TIMEOUT=900 #900 SEC 15 MIN
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'