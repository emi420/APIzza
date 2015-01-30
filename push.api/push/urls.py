from django.conf.urls import patterns, include, url
import settings

urlpatterns = patterns('',
    url(r'^installations/$', 'push.views.installations'),
    url(r'^installations/(.*)/$', 'push.views.install_get_one'),
    url(r'^push/$', 'push.views.push')
)


