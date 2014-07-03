from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^create/$', 'file.views.create'),
    url(r'^createBase64/$', 'file.views.createBase64'),
    url(r'^delete/(.*)/$', 'file.views.delete'),  
    url(r'^(.*)/$', 'file.views.get')
)
