import os
import sys
import site

site.addsitedir('/var/www/data.voolks.com/ENV/lib/python2.7/site-packages')
sys.path.append('/var/www/data.voolks.com')
sys.path.append('/var/www/data.voolks.com/data')

os.environ['DJANGO_SETTINGS_MODULE'] = 'data.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
