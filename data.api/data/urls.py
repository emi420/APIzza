from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^classes/(.*)/(.*)/$', 'data.views.classes_get_one'),
    url(r'^classes/(.*)/$', 'data.views.classes'),
)
