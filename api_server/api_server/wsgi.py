"""
WSGI config for api_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("EXTERNAL_CONFIG", "/var/www/apache_config/external_configs/api")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_server.settings.prod")

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
