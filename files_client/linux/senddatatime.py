import urllib2
import subprocess
import datetime
timenow =  datetime.datetime.now()
print timenow
t= open('time.txt')
r = t.readline()[:-1]
time = int(r)

finaltime = timenow+datetime.timedelta(0,0,0,0,time)
i = 0 
print finaltime
while datetime.datetime.now() < finaltime:
    i=i+1
    print datetime.datetime.now()
    print finaltime
    subprocess.call('~/bndwdth.sh',shell=True)
    addstr = "?"
    t=open('AvgPacketSec.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"avgpacsec="+r+"&"
    t=open('AvgPacketSize.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"avgpacsize="+r+"&"
    t=open('AvgPacketSecDwn.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"avgpacsecdwn="+r+"&"
    t=open('AvgPacketSizeDwn.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"avgpacsizedwn="+r+"&"
    t=open('BwdthKbps.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"bw="+r+"&"
    t=open('BwdthKbpsDwn.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"bwdwn="+r+"&"
    t=open('TotalClientPacket.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"totalclientpac="+r+"&"
    t=open('TotalClientPacketDwn.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"totalclientpacdwn="+r+"&"
    t=open('40-79.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_40_79="+r+"&"
    t=open('40-79Dwn.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_40_79dwn="+r+"&"
    t=open('80-159.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_80_159="+r+"&"
    t=open('80-159Dwn.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_80_159dwn="+r+"&"
    t=open('160-319.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_160_319="+r+"&"
    t=open('160-319Dwn.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_160_319dwn="+r+"&"
    t=open('320-639.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_320_639="+r+"&"
    t=open('320-639Dwn.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_320_639dwn="+r+"&"
    t=open('640-1279Dwn.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_640_1279="+r+"&"
    t=open('640-1279.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_640_1279dwn="+r+"&"
    t=open('2560-5119.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_2560_5119="+r+"&"
    t=open('2560-5119Dwn.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_2560_5119dwn="+r+"&"
    t=open('1280-2559.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_1280_2559dwn="+r+"&"
    t=open('1280-2559.csv')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"_1280_2559="+r+"&"
    t=open('SimId.txt')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"simid="+r+"&"
    t=open('PcId.txt')
    r=t.readline()[:-1]
    if r=="":
        r="0"
    addstr=addstr+"pcid="+r+"&"
    addstr=addstr+"dataid="+str(i)
    


    url = 'http://10.129.200.177:8000/monitor/test/'
    url = url+addstr
    req = urllib2.Request(url)
    print url
    req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36')
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding','gzip,deflate,sdch')
    req.add_header('Connection','keep-alive')
    req.add_header('Host','10.4.224.7:8000')
    
    res = urllib2.urlopen(req)
    print res.read()
