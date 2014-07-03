import os
import sys
import site

site.addsitedir('/var/www/file.voolks.com/ENV/lib/python2.7/site-packages')
sys.path.append('/var/www/file.voolks.com')
sys.path.append('/var/www/file.voolks.com/file')

os.environ['DJANGO_SETTINGS_MODULE'] = 'file.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
