from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse
import subprocess
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from netemapp.models import host
from netemapp.models import simulation,simulation_params
import datetime
from datetime import date
from django.template import RequestContext
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.

def group_required(*group_names):    
    """Requires user membership in at least one of the groups passed in."""    
    """def in_groups(u):       
        if u.is_authenticated():            
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True        
            return False    
    return user_passes_test(in_groups,login_url='/app/denied/')
    """
    return True

#@group_required('admin')
def home(request):
	allhosts=host.objects.all()[:10]	
	print {'hosts':allhosts}
	return render_to_response('netemapp/templates/netem.html',{'hosts':allhosts})

def test(request):    
    now = datetime.datetime.now()
    datestring=""
    datestring=datestring+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
    datestring= datestring+"*"
    to_sim=[]
    to_sim=request.POST.getlist("hostid")
    #selectedhosts=request.POST.getlist("hostid")
    simid = ""
    for hosts in to_sim:#selectedhosts:
        simid=simid+hosts+'!'
    simid=simid[0:-1]
    simid = datestring+simid
    print simid
    allhosts=host.objects.all()[:10]
    #pcarr = []
    #for hosts in selectedhosts:
        #data = host.objects.get(pk=hosts)
        #temp = {}
        #temp['id']=data.id
        #temp['ip']=data.hostip
        #temp['iface']=data.hostiface
        #pcarr.append(temp)
    #print pcarr
    #return render_to_response('netemapp/templates/test.html',{'hostdata':pcarr,'simid':simid})
    return render_to_response('netemapp/templates/sim.html',{'pc':to_sim,'hosts':allhosts,'simid':simid})

#group_required('admin')
def result(request):
    simidd = request.POST['simid']
    temp = simidd
    temp=temp.split('*')
    pcidarr = temp[1].split('!')
    for pcid in pcidarr:
        bwt = ""
        delay = ""
        loss = ""
        interface=""
        pcipobject = host.objects.get(pk=int(pcid))
        pcip = pcipobject.hostip
        for key in request.POST:
            print key
            if key=="simid":
                continue
            splitkey = key.split('*')
            print key
            print splitkey
            if splitkey[1]==pcid:
                if splitkey[0]=="bw":
                    bwt=request.POST[key]
                elif splitkey[0]=="loss":
                    loss = int(request.POST[key])
                elif splitkey[0]=="iface":
                    interface = request.POST[key]
                else: 
                    delay = request.POST[key]
        simparams = simulation_params(bw=int(bwt),delay=int(delay),loss=int(loss),iface=str(interface))
        simparams.save()
        simparamsid = simparams.id
        sim = simulation(simid=str(simidd),pcid=int(pcid),pcip=pcip,date_s= date.today(),simulationparams_id=simparamsid)
        sim.save()
        """elif key[:5]=="delay":
                sim = simulation(simid=simidd)
                print sim"""
    subprocess.call("assets/pre_test.sh",shell=True)
    for pcid in pcidarr:
        testpc = simulation.objects.get(simid=simidd,pcid=pcid)
        testpcparams = testpc.simulationparams
        subprocess.call("assets/multi_test.sh "+str(pcid)+" "+str(testpcparams.delay)+"ms "+str(testpc.pcip)+" "+str(testpcparams.bw)+"kbps "+str(testpcparams.loss),shell=True)
        print "bash called for "+pcid
    #subprocess.call("assets/testing.sh "+str(testpc.delay)+"ms "+str(testpc.loss)+" "+str(testpc.bw)+"kbps",shell=True)
    allpcsinsim = []
    allpcsinsim = simulation.objects.all().filter(simid__startswith=simidd)
    return render_to_response('netemapp/templates/result.html',{'allpc':allpcsinsim,'simid':simidd})

#group_required('admin')
def hostdbadd(request):
	context={}
	context.update(csrf(request))
	ip = request.POST["iprababu"]
	iface = request.POST["interface"]
	print ip
	add_host = host(hostip=ip,hostiface=iface)
	add_host.save()	
	return redirect(home)

#group_required('admin')
def hostintadd(request):
	formstring = ""+"<form action='simulation/hostdbadd/' method='POST'> IP of Host : <input type='text' name='iprababu'></br>Select Interface : <select name='interface'>"
	subprocess.call("assets/find_interface.sh",shell=True)		
	#print formstring+"\n"
	f=open('assets/interfaces.txt','r')
	#opening in read mode
	ints = f.readlines()
	f.close()
#ex: ['eth0\n','wlan0\n']
	print ints
	interfaces=[]
	for i in ints:
		i = i.split("\n")
		interfaces.append(i[0])	
	for inta in interfaces:
		formstring=formstring+"<option value='"+inta+"'>"+inta+"</option>"
	formstring=formstring+"<input type='submit' value='Add'></form>"
	return HttpResponse(formstring)

#group_required('admin')
def addpc(request):
	pcip = request.POST['pcip']
	pcname = request.POST['pcname']
	pcpass = request.POST['pcpass']
	pciface = request.POST['interface']
	pcmac = request.POST['mac']
	if len(pcmac)==0:
                print "findmac called"
		subprocess.call("assets/findmac.sh "+pcip,shell=True)
		l = open('assets/found_mac.txt','r')
                pcmac=l.readline()[:-1]
	addpc = host(hostip=pcip,hostname=pcname,hostpass=pcpass,hostiface=pciface,hostmac=pcmac)
	addpc.save()
        return HttpResponseRedirect('/simulation/add_del/')

#group_required('admin')
def add_del(request):
    c = {}
    c.update(csrf(request))
    allhosts=host.objects.all()[:10]
    i=0
    k=0
    for hosts in allhosts:
        k=k+1
    print i
    print "users"
    sys=i
    subprocess.call("assets/find_interface.sh",shell=True)		
	#print formstring+"\n"
    f=open('assets/interfaces.txt','r')
	#opening in read mode
    ints = f.readlines()
    f.close()
#ex: ['eth0\n','wlan0\n']
    print ints
    interfaces=[]
    for i in ints:
        i = i.split("\n")
        interfaces.append(i[0])				
        c.update({'hosts':allhosts,'interfaces':interfaces,'sys':sys,'i':k})
    return render_to_response('netemapp/templates/add_del_pc.html',c)

#group_required('admin')
def delpc(request):
    to_del = []
    to_del = request.POST.getlist('delid')
    #to_del = request.POST.getlist('pclist')
    print to_del
    print "sec"
    for ids  in to_del:
        print "hello"
        host.objects.filter(id=int(ids)).delete()
        print "hi"        
	#return HttpResponseRedirect('/simulation/add_del/')
    return HttpResponseRedirect('/simulation/add_del/')

#group_required('admin')
def scannetwork(request):
        startip = request.GET["start"]
        endip = request.GET["end"]
	subprocess.call('assets/scanforpcs.sh '+startip+" "+endip,shell=True)
	t= open('assets/ip_mac.txt')
        r=t.readlines()
        ip_mac = []
        macadd=""
        ipadd=""
        for line in r:
             if r.index(line)%2==1:
                dicts={}
                macadd = line[:-1]
                dicts['ip']=ipadd
                dicts['mac']=macadd
                ip_mac.append(dicts)
                print dicts 
             else:
                ipadd = line[:-1]
                
	htprespo="<form id='addpc'>"	
	for d in ip_mac:
		htprespo=htprespo+"<input type='radio' name='addpc' value='"+d['mac']+"&"+d['ip']+"'>"+d['ip']+"<br>"
	htprespo=htprespo+"<button type='button' class='btn btn-primary' onclick='scanpcadd()'>Add</button>" 
	print ip_mac	
	return HttpResponse(htprespo)

#group_required('admin')
def update(request):
        pcid=request.POST['delid']
        print pcid
    	pc = host.objects.get(pk=pcid)
        pcip = pc.hostip
        pcipsplit = pcip.split('.')
        print pcipsplit
        subnet = pcipsplit[0]+"."+pcipsplit[1]+"."+pcipsplit[2]
        print subnet
        subprocess.call("assets/scanforpcs.sh "+subnet+".1 "+"255",shell=True)
        macid=pc.hostmac+"\n"
        print macid
        t=open('assets/ip_mac.txt')
        r=t.readlines()
        index=-1
        print r
        try:
            index=r.index(macid)
        except ValueError:
            return HttpResponse("Pc not found")
        print index
        pcip=r[index-1][:-1]
        print pcip
        pc.hostip=pcip
        pc.save()
        return HttpResponseRedirect('/simulation/add_del/')
        print "IP not in the subnet"

"""     for pcs in allpcs:
                print pcs.hostip
                subprocess.call("assets/pingonce.sh "+pcs.hostip,shell=True)
                print "called for "+pcs.hostip
	for pc in allpcs:
		mac = pc.hostmac
                print mac
                mac = mac.lower()
		subprocess.call("assets/findip_frommac.sh "+mac,shell=True)
		t= open('assets/foundip_frommac.txt','r')
		ip=t.readline()[1:-2]
                print ip
		if not ip:
			htprespo=htprespo+pc.hostip+" not reachable!<br>"
                elif ip==pc.hostip:
			htprespo=htprespo+pc.hostname+"@"+pc.hostip+" already upto date.<br>"
                elif ip!=pc.hostip:
			htprespo=htprespo+"Updated "+pc.hostname+"@"+pc.hostip+" to "+pc.hostname+"@"+ip+"<br>"
			newpc = host.objects.get(pk=pc.id)
			newpc.hostip=ip
			newpc.save()"""
            
#group_required('admin')
def checkpc(request):
        ip = request.GET['ip']
        print ip
        p = subprocess.call("ping -c 1 "+ip+" | awk '/packet loss/ {print $4}'> /home/sampath/gitrepos/django/netemul/assets/checkpc.txt",shell=True)
        f = open('assets/checkpc.txt')
        r=f.readline()
        p=r[:-1]
        if p=='1':
            return HttpResponse("up")
        else:
            return HttpResponse("down")

#group_required('admin')
def upch(request):
    context = RequestContext(request)
    return render_to_response("netemapp/templates/updatepc.html",context)

#group_required('admin')
def giveparameters(request):
    context = RequestContext(request)
    return render_to_response("netemapp/templates/giveparameters.html",context)

def giveparameters2(request):
    context = RequestContext(request)
    return render_to_response("netemapp/templates/giveparameters2.html",context)

#group_required('admin')
def sim(request):
    context = RequestContext(request)
    to_sim = []
    to_sim = request.GET.getlist('hostid')
    print "to sim value:"
    print to_sim
    allhosts=host.objects.all()[:10]
    #print to_sim
    #pcid=request.POST.get('param')
    #for pcs in to_sim:
        #pcss=host.objects.filter(id=int(pcs))   
        #pcss = host.objects.get(pk=pcs)
        #print pcss.id
    #print "hi"
    #print pcss.id
    #if pcid=="1":
        #return render_to_response('netemapp/templates/sim.html',{'pc':to_sim,'pcid':pcid,'hosts':allhosts})
    #elif pcid=="2":
        #return render_to_response('netemapp/templates/sim.html',{'pc':to_sim,'pcid':pcid,'hosts':allhosts}) 
    return render_to_response('netemapp/templates/sim.html',{'pc':to_sim,'hosts':allhosts})
    #return render_to_response('netemapp/templates/sim.html',{})

#group_required('admin')
def delb(request):
    context = RequestContext(request)
    hid = request.GET['did']
    host.objects.filter(id=int(hid)).delete()
    strr=""+"<p style='color:green'>User is deleted</p>"
    return HttpResponse(strr)

#group_required('admin')
def updatepcinfo(request):
    pid1 = request.GET["pid"]
    hosts=host.objects.get(pk=int(pid1))
    #return render_to_response('netemapp/templates/updatepc.html',{'pid1':pid1,'hosts':hosts})
    #pid2=""+"<form id='addform' class='form-horizontal' action='/simulation/up/?id1="+pid1+"', method='post' onsubmit='return try2()'><br><br>"
    #pid2=pid2+"PC Name:<input type='text' name='pcname1' id='pcname1' placeholder='IP name' style='height:30px;' value='"+hosts.hostname+"'><br><br>"
    #pid2=pid2+"Password:<input type='password' name='pcpass1' id='pcpass1' placeholder='Password' style='height:30px;' value='"+hosts.hostpass+"'><br><br>"
    #pid2=pid2+"Interface:<select class='selectpicker' name='interface1' id='interface1' style='height:30px;'><option value='eth0'>eth0</option><option value='wlan0'>wlan0</option></select><br><br>"
    #pid2=pid2+"<input type='hidden' name='id1' id='id1' value='"+hosts.id+"'><br>"
    #pid2=pid2+"<input type='submit' class='btn btn-primary' value='Update'></form>"
    context = RequestContext(request)
    #return HttpResponse(pid2)
    return render_to_response("netemapp/templates/updatepc.html",{'pid':pid1,'host':hosts})

#group_required('admin')
def up(request):
    #pcname = request.POST['pcname']
    #pcpass = request.POST['pcpass']
    #pciface = request.POST['interface']
    id1 = request.GET["id1"]
    hosts = host.objects.all()
  # user is posting: get edited node, change comment, and save
    
    edited_host = hosts.get(id=int(id1))
    edited_host.hostname = request.GET['pcname1']
    edited_host.hostpass = request.GET['pcpass1']
    edited_host.hostifaace = request.GET['interface1']
    edited_host.save()
    strr=""+"<p style='color:green'>Updated successfully</p>"
    return HttpResponse(strr)
    #return HttpResponseRedirect('/simulation/add_del/')

#group_required('admin')
def check(request):
    return HttpRespone("done")
    to_sim = []
    to_sim = request.GET['delid']
    if to_sim=="":
        return HttpResponse("select")
    else:
        return HttpResponse("selected")
    return HttpRsponse("failure")

#login_required(login_url='/app/login/')
def graph(request):
    context = RequestContext(request)
    return render_to_response("netemapp/templates/graph.html",context)

#group_required('admin')
def showid(request):
    date1 = request.GET['date1']
    dater=simulation.objects.filter(date_s=date1)
    if dater:
        return render_to_response("netemapp/templates/graphd.html",{'data':dater,'date_s':date1})
    else:        
        strr=""+"<p style='color:red'>No simulations on the given day</p>"
        return HttpResponse(strr)
    return render_to_response("netemapp/templates/graph.html",{'data':dater})

#group_required('admin')
def monitor(request):
    context = RequestContext(request)
    to_sim = []
    to_sim = request.POST.getlist('hostid')
    allhosts=host.objects.all()[:10]
    return render_to_response('netemapp/templates/monitor.html',{'pc':to_sim,'hosts':allhosts})
#group_required('admin')
def add_del1(request):
    c = {}
    c.update(csrf(request))
    allhosts=host.objects.all()[:10]
    i=0
    k=0
    for hosts in allhosts:
        k=k+1
    print i
    print "users"
    sys=i
    subprocess.call("assets/find_interface.sh",shell=True)		
	#print formstring+"\n"
    f=open('assets/interfaces.txt','r')
	#opening in read mode
    ints = f.readlines()
    f.close()
#ex: ['eth0\n','wlan0\n']
    print ints
    interfaces=[]
    for i in ints:
        i = i.split("\n")
        interfaces.append(i[0])				
        c.update({'hosts':allhosts,'interfaces':interfaces,'sys':sys,'i':k})
    return render_to_response('netemapp/templates/add_del_pc1.html',c)
#group_required('admin')
def add_del2(request):
    c = {}
    c.update(csrf(request))
    allhosts=host.objects.all()[:10]
    i=0
    k=0
    for hosts in allhosts:
        k=k+1
    print i
    print "users"
    sys=i
    subprocess.call("assets/find_interface.sh",shell=True)		
	#print formstring+"\n"
    f=open('assets/interfaces.txt','r')
	#opening in read mode
    ints = f.readlines()
    f.close()
#ex: ['eth0\n','wlan0\n']
    print ints
    interfaces=[]
    for i in ints:
        i = i.split("\n")
        interfaces.append(i[0])				
        c.update({'hosts':allhosts,'interfaces':interfaces,'sys':sys,'i':k})
    return render_to_response('netemapp/templates/add_del_pc2.html',c)
#group_required('admin')
def addpc1(request):
	pcip = request.POST['pcip']
	pcname = request.POST['pcname']
	pcpass = request.POST['pcpass']
	pciface = request.POST['interface']
	pcmac = request.POST['mac']
	if len(pcmac)==0:
                print "findmac called"
		subprocess.call("assets/findmac.sh "+pcip,shell=True)
		l = open('assets/found_mac.txt','r')
                pcmac=l.readline()[:-1]
	addpc = host(hostip=pcip,hostname=pcname,hostpass=pcpass,hostiface=pciface,hostmac=pcmac)
	addpc.save()
        return HttpResponseRedirect('/simulation/add_del1/')
#@group_required('admin')
def addpc2(request):
	pcip = request.POST['pcip']
	pcname = request.POST['pcname']
	pcpass = request.POST['pcpass']
	pciface = request.POST['interface']
	pcmac = request.POST['mac']
	if len(pcmac)==0:
                print "findmac called"
		subprocess.call("assets/findmac.sh "+pcip,shell=True)
		l = open('assets/found_mac.txt','r')
                pcmac=l.readline()[:-1]
	addpc = host(hostip=pcip,hostname=pcname,hostpass=pcpass,hostiface=pciface,hostmac=pcmac)
	addpc.save()
        return HttpResponseRedirect('/simulation/add_del2/')

