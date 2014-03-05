from django.conf.urls import url, patterns, include
from django.contrib import admin 
import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
    url(r'^users/login/$', 'auth.views.login'),
    url(r'^users/signup/$', 'auth.views.signup'),
    url(r'^users/validate/(.*)/$', 'auth.views.validate_session'),
    url(r'^admin/', include(admin.site.urls)),
)

