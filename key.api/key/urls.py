from django.conf.urls import patterns, include, url
from rest_framework import viewsets, routers
from django.contrib import admin

admin.autodiscover()

router = routers.DefaultRouter()

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^check_key/$', 'key.views.check_key'),
    url(r'^create_key/$', 'key.views.create_key'),
    url(r'^delete/$', 'key.views.delete'),
    url(r'^key/admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls))
)
