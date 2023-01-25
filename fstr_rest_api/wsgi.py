import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fstr_rest_api.settings')

application = get_wsgi_application()
