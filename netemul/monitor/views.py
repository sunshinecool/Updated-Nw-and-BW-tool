from django.shortcuts import render
from netemapp.models import host
from netemapp.models import simulation
from monitor.models import monitorupload
from monitor.models import monitordownload,MonthlyWeatherByCity,charts_bw
from monitor.models import bw_upload_download,piedown
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import paramiko
from django.http import HttpResponse,StreamingHttpResponse
import json
import datetime
import subprocess
from datetime import date
#from django_socketio import events
from django.contrib.auth.decorators import login_required,user_passes_test
from chartit import DataPool, Chart
# Create your views here.
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in.
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
            return False
    return user_passes_test(in_groups,login_url='/app/denied/')"""
    return True

#@group_required('admin')
def home(request):
    simuid = request.GET['simid']
    print simuid
    allhosts = simulation.objects.filter(simid__startswith=simuid)
    return render_to_response('monitor/templates/socket.html',{'hosts':allhosts,'simid':simuid})

def livedata(request):
    simid = request.GET['simid']
    pcid = request.GET['pcid']
    data = []
    data = bw_upload_download.objects.filter(simid__exact=simid)
    data = data.filter(pcid__exact=int(pcid))
    length = len(data)-1
    print length
    dict = {}
    dict['bwup']= data[length].bw_upload
    dict['bwdown']=data[length].bw_download
    dict['pcid']=pcid 
    respo = json.dumps(dict)
    return HttpResponse(respo)

def testing(request):
    return render_to_response('monitor/templates/socket.html')

def simtomon(request):
    simuid=request.GET['simid']
    print simuid
    allpc = simulation.objects.filter(simid=simuid)
    print allpc
    return render_to_response('monitor/templates/monitor.html',{'hosts':allpc,'monid':simuid})

def lstest(request):
    testid = request.GET['id']
    realid = testid
    print testid
    testid = testid.split('@')
    pcid = testid[0]
    simid = testid[1]
    print testid
    print "ID recieved "+pcid+simid
    pc = host.objects.get(pk=pcid)
    user=pc.hostname
    pas=pc.hostpass
    ip=pc.hostip
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy())
    print "ssh establishing with "+user+ " " +pas+" "+ip+"\n"
    ssh.connect(hostname=ip,username=user,password=pas)
    stdin,stdout,stderr=ssh.exec_command("uname -a > ~/uname.txt")
    ssh.exec_command("echo '"+simid+"' > SimId.txt")
    print "simid done"
    print "pcid done"
    ssh.exec_command("echo '"+pcid+"' > PcId.txt")
    stdin,stdout,stderr = ssh.exec_command("python senddata.py & echo $! > pid.txt")
    r=stdout.readlines()
    ssh.close()
    print "dead"
    return HttpResponse("") 

def lstimetest(request):
    time = request.GET['time']
    testid = request.GET['id']
    realid = testid
    print testid
    testid = testid.split('@')
    pcid = testid[0]
    simid = testid[1]
    print testid
    print "ID recieved "+pcid+simid
    pc = host.objects.get(pk=pcid)
    user=pc.hostname
    pas=pc.hostpass
    ip=pc.hostip
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy())
    print "ssh establishing with "+user+ " " +pas+" "+ip+"\n"
    ssh.connect(hostname=ip,username=user,password=pas)
    stdin,stdout,stderr=ssh.exec_command("uname -a > ~/uname.txt")
    ssh.exec_command("echo '"+simid+"' > SimId.txt")
    print "simid done"
    print "pcid done"
    ssh.exec_command("echo '"+pcid+"' > PcId.txt")
    ssh.exec_command("echo '"+time+"' > time.txt")
    stdin,stdout,stderr = ssh.exec_command("python senddatatime.py & echo $! > pid.txt")
    r=stdout.readlines()
    ssh.close()
    print "dead"
    return HttpResponse("") 

def newlstest(request):
    testid = request.GET['id']
    realid = testid
    print testid
    testid = testid.split('@')
    pcid = testid[0]
    simid = testid[1]
    pc = host.objects.get(pk=pcid)
    user=pc.hostname
    pas=pc.hostpass
    ip=pc.hostip
    subprocess.call("echo 1 > assets/"+realid+".txt",shell=True)
    print realid
    i=0
    while True:
        t=open("assets/"+realid+".txt")
        r=t.readline()[:-1]
        if r==str(1):
            print "ada"
            subprocess.call("bash assets/Cmonitor.sh "+ip,shell=True)

            t=open('assets/Tests/BandwdthDown0-.csv')
            bndwdtdown=t.readline()[:-1]
            if bndwdtdown=="":
                bndwdtdown="0"
            print bndwdtdown
            
            t=open('assets/Tests/BandwdthUp0-.csv')
            bndwdtup=t.readline()[:-1]
            if bndwdtup=="":
                bndwdtup=="0"
            print bndwdtup
            
            bw_up_down = bw_upload_download(
                                      simid = simid,
                                      pcid = int(pcid),
                                      total_pkts_upload = 0,
                                      avg_pkts_upload = 0,
                                      avg_pkts_size_upload = 0,
                                      bw_upload = float(bndwdtup),
                                      total_pkts_download = 0,
                                      avg_pkts_download = 0,
                                      avg_pkts_size_download = 0,
                                      bw_download = float(bndwdtdown),
                                      dataid = int(i))
            i=i+1
            bw_up_down.save()
            print i

        else:
            return HttpResponse("") 


def kill(request):    
    testid = request.GET['id']
    realid = testid
    testid = testid.split('@')
    pcid = testid[0]
    simid = testid[1]
    pc = host.objects.get(pk=pcid)
    user=pc.hostname
    pas=pc.hostpass
    ip=pc.hostip
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy())
    print "ssh establishing with "+user+ " " +pas+" "+ip+"\n"
    ssh.connect(hostname=ip,username=user,password=pas)
    stdin,stdout,stderr = ssh.exec_command("python kill.py")
    ssh.close()
    return HttpResponse("")

def newkill(request):
    testid = request.GET['id']
    subprocess.call("echo 0 > assets/"+testid+".txt",shell=True)
    return HttpResponse("")


def test(request):
    getparams= request.GET
    monitorup = monitorupload(simid=request.GET['simid'],
                              pcid=int(request.GET['pcid']),
                              _40_79=float(request.GET['_40_79']),
                              _80_159=float(request.GET['_80_159']),
                              _160_319=float(request.GET['_160_319']),
                              _320_639=float(request.GET['_320_639']),
                              _640_1279=float(request.GET['_640_1279']),
                              _1280_2559=float(request.GET['_1280_2559']),
                              _2560_5119=float(request.GET['_2560_5119']),
                              dataid = int(request.GET['dataid']))
    monitorup.save()

    monitordw = monitordownload(simid=request.GET['simid'],
                              pcid=int(request.GET['pcid']),
                              _40_79=float(request.GET['_40_79dwn']),
                              _80_159=float(request.GET['_80_159dwn']),
                              _160_319=float(request.GET['_160_319dwn']),
                              _320_639=float(request.GET['_320_639dwn']),
                              _640_1279=float(request.GET['_640_1279dwn']),
                              _1280_2559=float(request.GET['_1280_2559dwn']),
                              _2560_5119=float(request.GET['_2560_5119dwn']),
                              dataid = int(request.GET['dataid']))
    monitordw.save()

    bw_up_down = bw_upload_download(
                              simid = request.GET['simid'],
                              pcid = int(request.GET['pcid']),
                              total_pkts_upload = float(request.GET['totalclientpac']),
                              avg_pkts_upload = float(request.GET['avgpacsec']),
                              avg_pkts_size_upload = float(request.GET['avgpacsize']),
                              bw_upload = float(request.GET['bw']),
                              total_pkts_download = float(request.GET['totalclientpacdwn']),
                              avg_pkts_download = float(request.GET['avgpacsecdwn']),
                              avg_pkts_size_download = float(request.GET['avgpacsizedwn']),
                              bw_download = float(request.GET['bwdwn']),
                              dataid = int(request.GET['dataid']))
    bw_up_down.save()

#    chartsbw =charts_bw(
#                            simid = request.GET['simid'],
#                            pcid = int(request.GET['pcid']),
#                            dataid = int(request.GET['dataid']),
#                            bw_upload = float(request.GET['bw']),
#                            bw_down = float(request.GET['bwdwn']),
#                        )
#
#    chartsbw.save()
    return HttpResponse("")

def directmon(request):
    now = datetime.datetime.now() 
    datestring="" 
    datestring=datestring+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second) 
    datestring= datestring+"*" 
    selectedhosts=[] 
    selectedhosts=request.POST.getlist("hostid") 
    simid = "" 
    print selectedhosts
    print "yehaf"
    for hosts in selectedhosts: 
        simid=simid+hosts+'!' 
    simid=simid[0:-1] 
    simid = datestring+simid 
    print date.today()
    for pc in selectedhosts:
	pcip = host.objects.get(pk=pc).hostip
        sim = simulation(simid=simid,pcid=pc,pcip=pcip,date_s=date.today())
        sim.save()
    return HttpResponseRedirect("/monitor/simtomon/?simid="+simid)

def chart_view(request):
    testid = request.GET['id']
    testid = testid.split('@')
    pcid = testid[0]
    simid = testid[1]
    data= bw_upload_download.objects.filter(simid__startswith=simid)
    data= data.filter(pcid__exact=pcid)
    print data
    avgpacpersec = DataPool(
               series=
                [{'options': {
                   'source': data},
                  'terms': [
                    'dataid',
                    'avg_pkts_upload',
                    'avg_pkts_download']}
                 ])

    #Step 2: Create the Chart object
    avgpaccht = Chart(
            datasource = avgpacpersec,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'dataid': [
                    'avg_pkts_upload',
                    'avg_pkts_download']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Average Packets per sec'},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})

    #Step 3: Send the chart object to the template.
   
    data = bw_upload_download.objects.filter(simid__startswith=simid)
    data = data.filter(pcid__exact=pcid)
    print data
    bwdata = DataPool(
               series=
                [{'options': {
                   'source': data},
                  'terms': [
                    'dataid',
                    'bw_upload',
                    'bw_download']}
                 ])
    #step 2: create the chart object
    bwcht = Chart(
            datasource = bwdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'dataid': [
                    'bw_upload',
                    'bw_download']
                  }}],
            chart_options =
              {'title': {
                   'text': 'bandwidth comparision'},
               'xaxis': {
                    'title': {
                       'text': 'time'}}})
    #Step 3: Send the chart object to the template.
    data = bw_upload_download.objects.filter(simid__startswith=simid)
    data = data.filter(pcid__exact=pcid)
    print data
    avgpacsize = DataPool(
               series=
                [{'options': {
                   'source': data},
                  'terms': [
                    'dataid',
                    'avg_pkts_size_upload',
                    'avg_pkts_size_download']}
                 ])
    #step 2: create the chart object
    avgpacsizecht = Chart(
            datasource = avgpacsize,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'dataid': [
                    'avg_pkts_size_upload',
                    'avg_pkts_size_download']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Average Packet Size comparision'},
               'xaxis': {
                    'title': {
                       'text': 'time'}}})
    #Step 3: Send the chart object to the template.
    data = monitordownload.objects.filter(simid__startswith=simid)
    data = data.filter(pcid__exact=pcid)
    leng = len(data)-1
    test = data[leng]
    arr = []
    dic = {}
    def getData():
	    dic['name']='40-79Kb'
	    dic['val']=test._40_79
	    arr.append(dic)
	    piedown(name='40-79Kb',val=test._40_79).save()
	    dic['name']='80-159Kb'
	    dic['val']=test._80_159
	    piedown(name='80-159Kb',val=test._80_159).save()
	    arr.append(dic)
	    dic['name']='160-319Kb'
	    dic['val']=test._160_319
            piedown(name='160-319Kb',val=test._160_319).save()
	    arr.append(dic)
	    dic['name']='320-639Kb'
	    dic['val']=test._320_639
	    arr.append(dic)
            piedown(name='320-639Kb',val=test._320_639).save()
	    dic['name']='640-1279Kb'
	    dic['val']=test._640_1279
	    arr.append(dic)
            piedown(name='640-1279Kb',val=test._640_1279).save()
	    dic['name']='1280-2559Kb'
	    dic['val']=test._1280_2559
            piedown(name='1280-2559Kb',val=test._1280_2559).save()
	    arr.append(dic)
	    dic['name']='2560-5119Kb'
	    dic['val']=test._2560_5119
	    arr.append(dic)     
            piedown(name='2560-5119Kb',val=test._2560_5119).save()

    getData()
    piec = DataPool(
               series=
                [{'options': {
                   'source':piedown.objects.all() },
                  'terms': [
                    'name',
                    'val']}
                 ])
    #step 2: create the chart object
    piecht = Chart(
            datasource = piec,
            series_options =
              [{'options':{
                  'type': 'pie',
                  'stacking': False},
                'terms':{
                  'name': [
                    'val']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Percentage of Packets'},
               'xaxis': {
                    'title': {
                       'text': 'time'}}})
 
    return render_to_response('monitor/templates/charts.html',{'chart1':[bwcht,avgpaccht,avgpacsizecht,piecht]})

