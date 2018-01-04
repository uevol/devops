import os
import sys
import django.core.handlers.wsgi
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Add this file path to sys.path in order to import settings
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devops.settings")

sys.stdout = sys.stderr

DEBUG = False

application = get_wsgi_application()
