from django.conf.urls import patterns, include, url 
from monitor import views 


urlpatterns = patterns('',
               url(r'^$', 'monitor.views.home', name='home'),
               url(r'^lstest/', 'monitor.views.lstest'),        
               url(r'^lstimetest/', 'monitor.views.lstimetest'),        
#               url(r'^getdata/', 'monitor.views.getdata'), 
               url(r'^test/', 'monitor.views.test'), 
               url(r'^simtomon/','monitor.views.simtomon'),
               url(r'^testing/', 'monitor.views.testing'), 
               url(r'^livedata/', 'monitor.views.livedata'), 
               url(r'^direcmon/','monitor.views.directmon'),
               url(r'^charts/','monitor.views.chart_view'),
               url(r'^kill/','monitor.views.kill'),
                 )
