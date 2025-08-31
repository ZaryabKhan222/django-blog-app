"""
Production settings for Django Blog on PythonAnywhere
"""
import os
from pathlib import Path
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update allowed hosts for your PythonAnywhere domain
ALLOWED_HOSTS = [
    'zaryabkhan.pythonanywhere.com',  # Replace with your actual domain
    'www.zaryabkhan.pythonanywhere.com',
]

# Static files configuration for PythonAnywhere
STATIC_URL = '/static/'
STATIC_ROOT = '/home/zaryabkhan/zaryabkhan.pythonanywhere.com/static/'

# Media files configuration for PythonAnywhere
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/zaryabkhan/zaryabkhan.pythonanywhere.com/media/'

# Database configuration (SQLite for PythonAnywhere free tier)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 86400
SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
CSRF_COOKIE_SECURE = False     # Set to True if using HTTPS

# Remove SSL redirect for free tier (no HTTPS)
SECURE_SSL_REDIRECT = False

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/zaryabkhan/zaryabkhan.pythonanywhere.com/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
