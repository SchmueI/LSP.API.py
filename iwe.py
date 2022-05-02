import time as waitTime
from time import time as utc_time
from datetime import datetime, time
import re
import requests
import codecs

def get_IWE(payload):

    with requests.Session() as s:                                                                                               #Neue Session erstellen
        r = s.post("https://www.landesschule-pforta.de/login.php", data=payload);
        cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}                                      #Friss den Cookie                                                                                             
        r = s.post('https://www.landesschule-pforta.de/intern/aktuell/iweAnmeldung.php', cookies=cookie, data=payload)          #Nutze cookie, um HiddenSite zu öffnen                                                                                                                     #Speichere Inhalt
        waitTime.sleep(2)
        cut=r.text.split('<h4 class="top18">Bisherige Anmeldungen</h4>', 1);                                                   #Erster Schnitt
        herr=0;
        iwestring="";
        try:
            final=cut[1].split("<!-- Ende Inhalt -->", 1);
        except IndexError:
            print("          {fetchHTML} >> Index Error. (Zugriffsfehler?)")
            return "Die IWE-Anmeldungen konnten nicht gelesen werden."
            herr=1
        if(herr==0):
            file3=open("iwe.html", "w+");                                                                         #Ausgabe der geschnittenen Datei in output-f.html
            file3.write(final[0]);                                                                                                  #Schreibe
            file3.close();                                                                                                          #Schließe Schreibdatei

            Zelle1="";
            Zelle2="";
            Zelle3="";
            z1=0;
            z2=0;
            z3=0;
            
            file4=open("iwe.html", "r");
            for line in file4:
                if '<div class="zelleAnm1">' in line.rstrip():
                    a=line.rstrip().split('<div class="zelleAnm1">', 1)
                    b=a[1].split('</div>')
                    Zelle1=b[0]
                    z1=1;
                    
                if '<div class="zelleAnm2">' in line.rstrip():
                    a=line.rstrip().split('<div class="zelleAnm2">', 1)
                    b=a[1].split('</div>')
                    Zelle2=b[0]
                    z2=1

                if '<div class="zelleAnm3">' in line.rstrip():
                    a=line.rstrip().split('<div class="zelleAnm3">', 1)
                    b=a[1].split('</div>')
                    Zelle3=b[0]
                    z3=1

                if '<div class="zelleAnm1 abstand8">' in line.rstrip():
                    a=line.rstrip().split('<div class="zelleAnm1 abstand8">', 1)
                    b=a[1].split('</div>')
                    Zelle1=b[0]
                    z1=1;
                    
                if '<div class="zelleAnm2 abstand8">' in line.rstrip():
                    a=line.rstrip().split('<div class="zelleAnm2 abstand8">', 1)
                    b=a[1].split('</div>')
                    Zelle2=b[0]
                    z2=1;
                    
                if '<div class="zelleAnm1 class="rot"">' in line.rstrip():
                    a=line.rstrip().split('<div class="zelleAnm1 class="rot"">', 1)
                    b=a[1].split('</div>')
                    Zelle1=b[0]
                    z1=1;
                    
                if '<div class="zelleAnm2 class="rot"">' in line.rstrip():
                    a=line.rstrip().split('<div class="zelleAnm2 class="rot"">', 1)
                    b=a[1].split('</div>')
                    Zelle2=b[0]
                    z2=1

                if '<div class="zelleAnm3 class="rot"">' in line.rstrip():
                    a=line.rstrip().split('<div class="zelleAnm3 class="rot"">', 1)
                    b=a[1].split('</div>')
                    Zelle3=b[0]
                    z3=1

                if '<div class="zelleAnm3 abstand8">' in line.rstrip():
                    a=line.rstrip().split('<div class="zelleAnm3 abstand8">', 1)
                    b=a[1].split('</div>')
                    Zelle3=b[0]
                    z3=1
                    
                if(z1 == 1):
                    if(z2 == 1):
                        if(z3==1):
                            z1=0;
                            z2=0;
                            #z3=0;
                            iwestring=""+iwestring+"\n"+Zelle1+"\n"+Zelle2+"\n";
            iwestring="Folgende Schüler haben sich *zum IWE angemeldet*\n"+iwestring
            return iwestring

def IWE_anmelden(wsuser, wspass, wszusatz):
    with requests.Session() as s:
        r = s.post("https://www.landesschule-pforta.de/login.php", data={'user':wsuser ,'pwd':wspass});
        cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}                                      #Friss den Cookie                                                                                                 
        r = s.post('https://www.landesschule-pforta.de/intern/aktuell/iweAnmeldung.php', cookies=cookie, data={'user':wsuser ,'pwd':wspass})          #Nutze cookie, um HiddenSite zu öffnen
        waitTime.sleep(2)
        r = s.post('https://www.landesschule-pforta.de/intern/aktuell/iweAnmeldung.php', cookies=cookie, data={'user':wsuser, 'pwd':wspass, 'aktion':'', 'aktion':'anmeldungBearbeiten'}) #Nutze Hiddenside um transid zu ermitteln
        waitTime.sleep(2)
        file=open("IWE.html", "w+");                                                                                        
        file.write(r.text);                                                                                                  
        file.close(); 
        file2=open("IWE.html", "r");
        transid="0"
        for line in file2:
            if '<input type="hidden" name="transid" value="' in line.rstrip():
                a=line.rstrip()
                b=a.split('<input type="hidden" name="transid" value="', 1)
                c=b[1].split('" />', 1)
                transid=c[0]
                #print(transid)
        if(transid=="0"):
            return  0
        else:
            r = s.post('https://www.landesschule-pforta.de/intern/aktuell/iweAnmeldung.php', cookies=cookie, data={'user':wsuser, 'pwd':wspass, 'aktion':'', 'transid':transid, 'zusatz':wszusatz, 'aktion':'anmeldungSpeichern'})
            return 1
        
def IWE_abmelden(wsuser, wspass):

    with requests.Session() as s:                                                                                                                                                         
        r = s.post("https://www.landesschule-pforta.de/login.php", data={'user':wsuser ,'pwd':wspass});
        cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}                                                                                                #Friss den Cookie                                                                                                    
        r = s.post('https://www.landesschule-pforta.de/intern/aktuell/iweAnmeldung.php', cookies=cookie, data={'user':wsuser ,'pwd':wspass})                                              #Nutze cookie, um HiddenSite zu öffnen
        waitTime.sleep(2)
        r = s.post('https://www.landesschule-pforta.de/intern/aktuell/iweAnmeldung.php', cookies=cookie, data={'user':wsuser, 'pwd':wspass, 'aktion':'', 'aktion':'anmeldungBearbeiten'}) #Nutze Hiddenside um transid zu ermitteln
        waitTime.sleep(2)
        file=open("IWE.html", "w+");                                                                                                                                     #Erstelle output.html
        file.write(r.text);                                                                                                                                                               #Schreibe HTML in Datei
        file.close(); 
        file2=open("IWE.html", "r");
        transid="0"
        for line in file2:
            if '<input type="hidden" name="transid" value="' in line.rstrip():
                a=line.rstrip()
                b=a.split('<input type="hidden" name="transid" value="', 1)
                c=b[1].split('" />', 1)
                transid=c[0]
        if(transid=="0"):
            return 0
        else:
            r = s.post('https://www.landesschule-pforta.de/intern/aktuell/iweAnmeldung.php', cookies=cookie, data={'user':wsuser, 'pwd':wspass, 'aktion':'', 'transid':transid, 'aktion':'anmeldungLoeschen'}) 
            return 1