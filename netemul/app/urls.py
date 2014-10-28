from django.conf.urls import patterns, include, url
#from app.views import hello
#from app.views import login
#from app.views import register
#from app import views
#from app.views import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'octo.views.home', name='home'),
    # url(r'^octo/', include('octo.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     
     
       
      
      url(r'^register/$', 'app.views.register', name='register'), 
      url(r'^login/$', 'app.views.user_login', name='login'),  
      #url(r'^home_admin/$', 'app.views.home_admin', name='home_admin'),  
      #url(r'^home_guest/$', 'app.views.home_guest', name='home_guest'),
      #url(r'^submit_pc/$', 'app.views.submit_pc', name='submit_pc'),
      #url(r'^pcdetails/$', 'app.views.pcdetails', name='pcdetails'),
      #url(r'^showpcdetails/$', 'app.views.showpcdetails', name='showpcdetails'),
      url(r'^showguests/$', 'app.views.showguests', name='showguests'),
      #url(r'^restricted/', 'app.views.restricted', name='restricted'),
      url(r'^logout/$', 'app.views.user_logout', name='logout'),
      #url(r'^deletepc/$', 'app.views.deletepc', name='deletepc'),
      url(r'^authdemo/$', 'app.views.authdemo', name='authdemo'),
      url(r'^denied/$', 'app.views.denied', name='denied'),
      url(r'^admin/$', 'app.views.admin', name='home'),
      url(r'^hi/$', 'app.views.hi', name='hi'),
      url(r'^home/$', 'app.views.home', name='home1'),
      url(r'^passc/$', 'app.views.passc', name='passc'),
      url(r'^delu/$', 'app.views.delu', name='delu'),
      url(r'^managesys/$', 'app.views.managesys'),
      #url(r'^managesystems/$', 'app.views.managesystems')
      #url(r'^reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','app.views.reset_confirm', name='reset_confirm'),
      #url(r'^reset/$', 'app.views.reset','django.contrib.auth.views.password_reset'),
      #url(r'^password_reset_form/$','app.views.password_reset_form',name='password_reset_form'),
      
)
urlpatterns += staticfiles_urlpatterns()
