from django.conf.urls import patterns, include, url
import settings

urlpatterns = patterns('',
    url(r'^savegeo/$', 'geo.views.savegeo'),
    url(r'^neargeo/$', 'geo.views.neargeo'),
    url(r'^withingeo/$', 'geo.views.withingeo')
)


