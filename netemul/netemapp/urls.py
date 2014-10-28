from django.conf.urls import patterns, include, url
from netemapp import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'netemapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^test/', 'netemapp.views.test'),
    #url(r'^ajaxfunc/', 'netemapp.views.ajaxfunc'),
   # url(r'^admin/', include(admin.site.urls)),
    url(r'^sim/','netemapp.views.sim'),
    url(r'^netem/','netemapp.views.home'),
    url(r'^hostdbadd/', 'netemapp.views.hostdbadd'),
    url(r'^result/', 'netemapp.views.result'),
    url(r'^hostintadd/', 'netemapp.views.hostintadd'),
    url(r'^add_del/','netemapp.views.add_del'),
    url(r'^delpc/','netemapp.views.delpc'),
    url(r'^addpc/','netemapp.views.addpc'), 
    url(r'^addpc2/','netemapp.views.addpc2'),
    url(r'^addpc1/','netemapp.views.addpc1'),
    url(r'^scanforpc/','netemapp.views.scannetwork'),
    url(r'^updatepc/','netemapp.views.update'),
    url(r'^giveparameters/','netemapp.views.giveparameters'),
    url(r'^giveparameters2/','netemapp.views.giveparameters2'),    
    url(r'^checkpc/','netemapp.views.checkpc'),
    url(r'^upch/','netemapp.views.upch'),
    url(r'^delb/','netemapp.views.delb'),
    url(r'^updatepcinfo/','netemapp.views.updatepcinfo'),
    url(r'^up/','netemapp.views.up'),
    url(r'^check/','netemapp.views.check'),
    url(r'^graph/','netemapp.views.graph'),
    url(r'^showid/','netemapp.views.showid'),
    url(r'^monitor/','netemapp.views.monitor'),
    url(r'^add_del1/','netemapp.views.add_del1'),
    url(r'^add_del2/','netemapp.views.add_del2'),
)
