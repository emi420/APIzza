from django.conf.urls import patterns, include, url
import settings

urlpatterns = patterns('',
    url(r'^savegeo/$', 'geo.views.savegeo')
)


