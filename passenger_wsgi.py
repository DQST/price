import sys, os
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + '/price')

os.environ['DJANGO_SETTINGS_MODULE'] = "price.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
