# FILE: medisoft/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('臨界_SETTINGS_MODULE', 'medisoft.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medisoft.settings')
application = get_wsgi_application()