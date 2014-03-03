from django.conf.urls import url, patterns, include
from django.contrib import admin 
import settings

admin.autodiscover()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
    url(r'^users/login/$', 'auth.views.login'),
    url(r'^users/validate_session/$', 'auth.views.validate_session'),
    url(r'^admin/', include(admin.site.urls)),
)

