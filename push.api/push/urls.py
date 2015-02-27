from django.conf.urls import patterns, include, url
import settings

urlpatterns = patterns('',
    url(r'^installations/$', 'push.views.installations'),
    url(r'^delete/$', 'push.views.delete'),
    url(r'^push/$', 'push.views.push'),
    url(r'^push/(.*)/$', 'push.views.push_one'),
)


