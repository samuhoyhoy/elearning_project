import os
from django.core.wsgi import get_wsgi_application

# set default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_project.settings')

# WSGI entry point 
application = get_wsgi_application()
