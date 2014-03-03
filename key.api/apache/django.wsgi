import os
import sys
import site

site.addsitedir('/var/www/key.voolks.com/ENV/lib/python2.7/site-packages')
sys.path.append('/var/www/key.voolks.com')
sys.path.append('/var/www/key.voolks.com/key')

os.environ['DJANGO_SETTINGS_MODULE'] = 'key.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
