from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.contrib.auth.models import Group,Permission
from django.http import Http404
from app.models import Blog
from app.models import User_login
#from app.forms import PostForm
from django.contrib.auth import authenticate, login
#from app.forms import LoginForm
from app.forms import UserForm
from app.forms import PcForm
from app.models import PcDetails
from django.contrib.auth.models import User,Group
from app.models import UserProfile
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.core.context_processors import csrf
#from app.models import UserProfile.user.username
from django.core.urlresolvers import reverse
#from django.contrib.auth.views import password_reset, password_reset_confirm


def group_required(*group_names):    
    """Requires user membership in at least one of the groups passed in."""    
    def in_groups(u):       
        if u.is_authenticated():            
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True        
            return False    
    return user_passes_test(in_groups,login_url='/app/denied/')

def denied(request):
    context = RequestContext(request)
    return render_to_response("app/templates/denied.html",context)
@group_required('admin')
def hi(request):
    context = RequestContext(request)
    return render_to_response("app/templates/hello.html",context)
@group_required('admin')
def hello(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/app/home/')
    else:
        context = RequestContext(request)
        return render_to_response("app/templates/login.html",context)
    #return HttpResponse("hello");

@group_required('admin')
def register(request):
 if request.user.is_authenticated():
   context = RequestContext(request)
   registered = False
   if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            #user.set_password(user.password)
            group = request.POST['Group']
            if group == '1':
                g = Group.objects.get(name='admin') 
                g.user_set.add(user)
            else:
                g = Group.objects.get(name='tester') 
                g.user_set.add(user)
            user.save()
            registered = True
            #strr=""+"alert('User is registerd')"
            #return HttpResponse(strr);
        else:
            print user_form.errors
   else:
        user_form = UserForm()
   return render_to_response(

            {'user_form': user_form,'registered': registered},
            context)
 else:
   return HttpResponseRedirect('/app/login/')
def user_login(request):
      if request.user.is_authenticated():
        return HttpResponseRedirect('/app/home/')
      context = RequestContext(request)
      if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
           
            if user.is_active:
                login(request, user)
                #group = Group.objects.get(name='admin')
                #users = group.user_set.all()
                #group1 = Group.objects.get(name='tester')
                #guestsdetails = group1.user_set.all()

                return HttpResponseRedirect("/app/home/")
                #return HttpResponseRedirect('/app/home/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            
            print "Invalid login details: {0}, {1}".format(username, password)
            msg = "Enter valid login details"
            context_dict = {
           'msg': msg,
            }
            return render_to_response('app/templates/login.html',context_dict,context)

      else:
        
        return render_to_response('app/templates/login.html', {}, context)

@login_required(login_url='/app/login/')
def home(request):
    context = RequestContext(request)
    group = Group.objects.get(name='admin')
    users = group.user_set.all()
    group1 = Group.objects.get(name='tester')
    guestsdetails = group1.user_set.all()
    return render_to_response("app/templates/home.html", {'users':users,'guestsdetails':guestsdetails}, context)
@group_required('admin')
def admin(request):
    context = RequestContext(request)
    return render_to_response("app/templates/admin.html", context)
  

@group_required('admin')
def showguests(request):
    context = RequestContext(request)
    guestsdetails = User.objects.all()
    group = Group.objects.get(name='tester')
    users = group.user_set.all()
    group1 = Group.objects.get(name='admin')
    guestsdetails = group1.user_set.all()

    return render_to_response("app/templates/showguests.html", {'users':users,'guestsdetails':guestsdetails}, context)
  
@login_required(login_url='/app/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/app/login/')
@group_required('admin')
def managesys(request):
   context = RequestContext(request)
   return render_to_response("app/templates/showguests.html", {'users':users,'guestsdetails':guestsdetails}, context) 
@group_required('admin')
def authdemo(request):
	admin_users = Group(name='admin')
	admin_users.save()
	tester_users = Group(name='tester')
	tester_users.save()
        return HttpResponse("done!!")
@group_required('admin')
def passc(request):
    context = RequestContext(request)
    passw=request.GET["npass"]
    print passw
    u = User.objects.get(username__exact=request.user.username)
    u.set_password(passw)
    print passw
    u.save()   
    print passw
    strr=""+"<p style='color:green'>Password changed Successfully!!</p>"     
    return HttpResponse(strr)
@group_required('admin')
def delu(request):
    hid = request.GET["hid"]
    User.objects.filter(id=int(hid)).delete()
    strr=""+"<p style='color:green'>Deleted Succcessfully</p>"
    return HttpResponse(strr)
