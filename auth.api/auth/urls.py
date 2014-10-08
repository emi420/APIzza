from django.conf.urls import url, patterns, include
from django.contrib import admin 
import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'auth.views.login'),
    url(r'^signup/$', 'auth.views.signup'),
    url(r'^validate/(.*)/$', 'auth.views.validate_session'),
    url(r'^permissions/$', 'auth.views.permissions'),
    url(r'^delete/$', 'auth.views.delete'),
    url(r'^users/admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls))
)

