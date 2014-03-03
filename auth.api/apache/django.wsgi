import site
import sys
import os

site.addsitedir('/var/www/auth.voolks.com/ENV/lib/python2.7/site-packages')
sys.path.append('/var/www/auth.voolks.com')
sys.path.append('/var/www/auth.voolks.com/auth')

os.environ['DJANGO_SETTINGS_MODULE'] = 'auth.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
