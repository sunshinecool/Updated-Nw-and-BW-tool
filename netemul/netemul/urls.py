from django.conf.urls import patterns, include, url
from netemapp import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
   # url(r'^$', 'netemapp.views.home', name='home'),
    url(r'^simulation/', include('netemapp.urls')),
    url(r'^admin/', include(admin.site.urls)), 
    url(r'^app/', include('app.urls')), 
    url(r'^monitor/', include('monitor.urls')), 
   )
