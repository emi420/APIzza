from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^upload/$', 'file.views.create'),
)
