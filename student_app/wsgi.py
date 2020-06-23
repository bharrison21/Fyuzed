"""
WSGI config for student_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_app.settings')

application = get_wsgi_application()


sys.path.append('/opt/bitnami/apps/django/django_projects/tutorial')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/tutorial/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()