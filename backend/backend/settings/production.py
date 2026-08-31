import os
from dotenv import load_dotenv

load_dotenv(".env.production")

from .base import *

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = [
    "djangostore.ru",
    "www.djangostore.ru",
    "localhost",
    "127.0.0.1",
    "backend-container",
    "::1",
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
CSRF_TRUSTED_ORIGINS = ["https://djangostore.ru", "https://www.djangostore.ru"]
# CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STATIC_URL = "/static/"
STATIC_ROOT = "/app/staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/app/media"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_LOCATION", None),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.getenv("REDIS_PASSWORD", None),
            "SOCKET_CONNECTION_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "RETRY_ON_TIMEOUT": True,
            "MAX_CONNECTIONS": 1000,
            "CONNECTION_POOL_CLASS": "redis.BlockingConnectionPool",
            "CONNECTION_POOL_CLASS_KWARGS": {
                "max_connections": os.getenv("REDIS_MAX_CONNECTIONS", 100),
                "timeout": os.getenv("REDIS_SOCKET_TIMEOUT", 10),
            }
        }
    },

    "sessions": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_LOCATION", None),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.getenv("REDIS_PASSWORD", None),
            "SOCKET_CONNECTION_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "RETRY_ON_TIMEOUT": True,
            "MAX_CONNECTIONS": 1000,
            "CONNECTION_POOL_CLASS": "redis.BlockingConnectionPool",
            "CONNECTION_POOL_CLASS_KWARGS": {
                "max_connections": os.getenv("REDIS_MAX_CONNECTIONS", 100),
                "timeout": os.getenv("REDIS_SOCKET_TIMEOUT", 10),
            }
        }
    }
}
