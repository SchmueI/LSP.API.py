import time as waitTime
from time import time as utc_time
from time import strftime
from datetime import datetime, time
import re
import requests
import codecs

def getConnection(station):
    h=str(datetime.now().time().hour) 
    m=str(datetime.now().time().minute)
    D=strftime("%d")
    M=strftime("%m")
    Y=strftime("%Y")[-2:]
    if(station in ["Pforte", "Pforta"]): url="https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=43176&country=DEU&protocol=https:&seqnr=7&ident=3g.013083176.1643976496&rt=1&input=Bad%20K%F6sen%20Schulpforte,%20Naumburg%20(Saale)%23960600&time="+str(h)+":"+str(m)+"&date="+D+"."+M+"."+Y+"&ld=43176&productsFilter=1111111111&start=1&boardType=dep&rtMode=DB-HYBRID&"
    elif(station == "Kaufhalle"): url="https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=43176&country=DEU&protocol=https:&seqnr=2&ident=dl.029560176.1643985159&rt=1&input=Bad%20K%F6sen%20Kaufhalle,%20Naumburg%20(Saale)%23960569&time="+str(h)+":"+str(m)+"&date="+D+"."+M+"."+Y+"&ld=43176&productsFilter=1111111111&start=1&boardType=dep&rtMode=DB-HYBRID&"
    elif(station == "Bad Kösen Bahnhof"): url= "https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=43176&country=DEU&protocol=https:&seqnr=3&ident=hj.0678176.1643989327&rt=1&input=Bad%20K%F6sen%20Bahnhof%20(Bus),%20Naumburg%20(Saale)%23959487&time="+str(h)+":"+str(m)+"&date="+D+"."+M+"."+Y+"&ld=43176&productsFilter=1111111111&start=1&boardType=dep&rtMode=DB-HYBRID&"
    elif(station == "Curt-Becker Platz"): url= "https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=43176&country=DEU&protocol=https:&seqnr=2&ident=dl.029560176.1643985159&rt=1&input=Curt-Becker-Platz%20(Bus),%20Naumburg%20(Saale)%23959454&time="+str(h)+":"+str(m)+"&date="+D+"."+M+"."+Y+"&ld=43176&productsFilter=1111111111&start=1&boardType=dep&rtMode=DB-HYBRID&"
    elif(station == "Naumburg Bahnhof"): url="https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=43176&country=DEU&protocol=https:&seqnr=3&ident=1p.017559176.1643990644&rt=1&input=Busbahnhof%20am%20Hauptbahnhof,%20Naumburg%20(Saale)%23960507&time="+str(h)+":"+str(m)+"&date="+D+"."+M+"."+Y+"&ld=43176&productsFilter=1111111111&start=1&boardType=dep&rtMode=DB-HYBRID&"
    else: return "Leider kenne ich diese Station nicht."

    with requests.Session() as s:
        r=s.post(url)
        waitTime.sleep(1)
        html=r.text
        html = html.replace("&#223;", "ß")
        html = html.replace("&#228;", "ä")
        html = html.replace("&#246;", "ö")
        value=""
        newEntity=""
        split=["","",""]
        for x in range (4):
            if('<tr id="journeyRow' in html): split=html.split('<tr id="journeyRow', 1)
            if('<td class="time">' in split[1]): time=split[1].split('<td class="time">',1)[1].split('</td>', 1)[0]
            if('<td class="time">' in split[1]): html=split[1].split('<td class="time">',1)[1].split('</td>', 1)[1]
            if(';">' in html): veh=html.split(';">', 2)[2].split('</a>', 1)[0][:-1][1:]
            if(';">' in html): html=html.split(';">', 2)[2].split('</a>', 1)[1]
            if('?input=' in html): dest=html.split('?input=', 1)[1].split('&', 1)[0]
            if("%" in dest): dest=dest.split('%', 1)[0]
            if('?input=' in html): html=html.split('?input=', 1)[1].split('&', 1)[1]
            if('">' in veh): veh=veh.split('">', 1)[1].split('<',1)[0]
            if not (newEntity == time + " " +  veh +" -> " + dest+"\n"):
                newEntity = time + " " +  veh +" -> " + dest+"\n"
                value=value+newEntity
    h=time[:2]
    m=int(time[-2:])+1
    if(station in ["Pforte", "Pforta"]): url="https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=43176&country=DEU&protocol=https:&seqnr=7&ident=3g.013083176.1643976496&rt=1&input=Bad%20K%F6sen%20Schulpforte,%20Naumburg%20(Saale)%23960600&time="+str(h)+":"+str(m)+"&date="+D+"."+M+"."+Y+"&ld=43176&productsFilter=1111111111&start=1&boardType=dep&rtMode=DB-HYBRID&"
    elif(station == "Curt-Becker Platz"): url= "https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=43176&country=DEU&protocol=https:&seqnr=2&ident=dl.029560176.1643985159&rt=1&input=Curt-Becker-Platz%20(Bus),%20Naumburg%20(Saale)%23959454&time="+str(h)+":"+str(m)+"&date="+D+"."+M+"."+Y+"&ld=43176&productsFilter=1111111111&start=1&boardType=dep&rtMode=DB-HYBRID&"
    elif(station == "Bad Kösen Bahnhof"): url= "https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=43176&country=DEU&protocol=https:&seqnr=3&ident=hj.0678176.1643989327&rt=1&input=Bad%20K%F6sen%20Bahnhof%20(Bus),%20Naumburg%20(Saale)%23959487&time="+str(h)+":"+str(m)+"&date="+D+"."+M+"."+Y+"&ld=43176&productsFilter=1111111111&start=1&boardType=dep&rtMode=DB-HYBRID&"
    elif(station == "Kaufhalle"): url="https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=43176&country=DEU&protocol=https:&seqnr=2&ident=dl.029560176.1643985159&rt=1&input=Bad%20K%F6sen%20Kaufhalle,%20Naumburg%20(Saale)%23960569&time="+str(h)+":"+str(m)+"&date="+D+"."+M+"."+Y+"&ld=43176&productsFilter=1111111111&start=1&boardType=dep&rtMode=DB-HYBRID&"
    elif(station == "Naumburg Bahnhof"): url="https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=43176&country=DEU&protocol=https:&seqnr=3&ident=1p.017559176.1643990644&rt=1&input=Busbahnhof%20am%20Hauptbahnhof,%20Naumburg%20(Saale)%23960507&time="+str(h)+":"+str(m)+"&date="+D+"."+M+"."+Y+"&ld=43176&productsFilter=1111111111&start=1&boardType=dep&rtMode=DB-HYBRID&"
    with requests.Session() as s:
        r=s.post(url)
        waitTime.sleep(1)
        html=r.text
        html = html.replace("&#223;", "ß")
        html = html.replace("&#228;", "ä")
        html = html.replace("&#246;", "ö")
        for x in range (4):
            if('<tr id="journeyRow' in html): split=html.split('<tr id="journeyRow', 1)
            if('<td class="time">' in split[1]): time=split[1].split('<td class="time">',1)[1].split('</td>', 1)[0]
            if('<td class="time">' in split[1]): html=split[1].split('<td class="time">',1)[1].split('</td>', 1)[1]
            if(';">' in html): veh=html.split(';">', 2)[2].split('</a>', 1)[0][:-1][1:]
            if(';">' in html): html=html.split(';">', 2)[2].split('</a>', 1)[1]
            if('?input=' in html): dest=html.split('?input=', 1)[1].split('&', 1)[0]
            if("%" in dest): dest=dest.split('%', 1)[0]
            if('?input=' in html): html=html.split('?input=', 1)[1].split('&', 1)[1]
            if('">' in veh): veh=veh.split('">', 1)[1].split('<',1)[0]
            if not (newEntity == time + " " +  veh +" -> " + dest+"\n"):
                newEntity = time + " " +  veh +" -> " + dest+"\n"
                value=value+newEntity

    return value 