"""
WSGI config for django_blog project on PythonAnywhere.
"""

import os
import sys

# Add the project directory to the Python path
path = '/home/zaryabkhan/zaryabkhan.pythonanywhere.com'
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings_production')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
