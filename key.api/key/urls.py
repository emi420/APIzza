from django.conf.urls import patterns, include, url
from rest_framework import viewsets, routers

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    # Examples:
    # url(r'^$', 'key.views.home', name='home'),
    # url(r'^key/', include('key.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^check_key/$', 'key.views.check_key'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
