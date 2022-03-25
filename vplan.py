import time as waitTime
from time import time as utc_time
from datetime import datetime, time
import re
import requests
import codecs

def get_plan(payload, typus):
    with requests.Session() as s:                                                                                                   #Neue Session erstellen
        try:
            r = s.post(https://www.landesschule-pforta.de/login.php, data=payload);
            waitTime.sleep(1)
            cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}                                      #Friss den Cookie                                                                                                 
            r = s.post('https://www.landesschule-pforta.de/intern/aktuell/vertretungsplan.php', cookies=cookie, data=payload)       #Nutze cookie, um HiddenSite zu öffnen
            htmlContents = r.text
            
            
        except UnboundLocalError:
            print("          {fetchHTML} >> "+str(datetime.now().time())+"Die Verweigerung des Zugriffs hatte einen Fehler zufolge.");
            pass;
        except requests.exceptions.ConnectionError:
            print("          {fetchHTML} >> "+str(datetime.now().time())+"'Ein Verbindungsversuch ist fehlgeschlagen, da die Gegenstelle nach einer bestimmten Zeitspanne nicht richtig reagiert hat, oder die hergestellte Verbindung war fehlerhaft, da der verbundene Host nicht reagiert hat");
        except ConnectionResetError:
            print("          {fetchHTML} >> "+str(datetime.now().time())+"Die Verbindung wurde geschlossen (socket.timeout)");
       
       
                   
        cut=htmlContents.split("Vertretungs- und Aufsichtspläne", 1);

        # This codeblock (which is yet a mess) is used to seperate the html contents
        final=["", ""]
        connErr=0;
        vPlanString="Konnte keine Verbindung zum Server aufbauen"
        try:
            final=cut[1].split("Aufsichtspläne", 1);
        except IndexError: 
            vPlanString="\nKonnte keine Verbindung zum Server aufbauen Vielleicht sind deine Zugangsdaten nicht korrekt?"
            connErr=1;
            print("          {fetchHTML} >> Zugriff verweigert.")
            pass
        file3=open("vplan.html", "w+");                                                                                             #Ausgabe der geschnittenen Datei in output-f.html
        file3.write(final[0]);                                                                                                      #Schreibe
        file3.close();                                                                                                              #Schließe Schreibdatei
        Stunde='';
        Klasse='';
        Fach='';
        Lehrer='';
        vLehrer='';
        vFach='';

        hatStunde=0;
        hatKlasse=0;
        hatFach=0;
        hatLehrer=0;
        hatvLehrer=0;
        hatvFach=0;
        hatAnmerkung=0;
             


        plain=open("vplan.txt", "w+", encoding='utf-8');                                                                            # This file contains the vPlan as string.txt (formatted)
        htmlCut=open("vplan.html", "r");                                                                                              # This file is used to be read line by line and formatted into telegram Markup
        if(connErr==0):
            vPlanString="";
        for line in htmlCut:                                                                                                          #Lese Zeile für Zeile aus
            if "Vertretungsplan für" in line.rstrip():                                                                              #Überschrift
                a=line.rstrip();
                b=a.split('<div class="boxHeadLeft"><b><span class="boxHeadAdd">', 1);
                c=b[1].split("</span>", 1);
                d=c[1].split("</b></div>", 1)
                e=''+d[0]+''+d[1];
                #print();  
                if("Montag" in e):
                    wTag="Montag"
                if("Dienstag" in e):
                    wTag="Dienstag"
                if("Mittwoch" in e):
                    wTag="Mittwoch"
                if("Donnerstag" in e):
                    wTag="Donnerstag"
                if("Freitag" in e):
                    wTag="Freitag"

                print("          {fetchHTML} >> "+wTag+" "+typus)

                if (typus == "V"): vPlanString=vPlanString+"\n\n<b>"+e+"</b>";
                        
                plain.write("\n\n"+e+"\nVertretungsplan:\n");
                
            if "<p><i>Für diesen Tag wurde noch kein Vertretungsplan hochgeladen.</i></p>" in line.rstrip():                                                                              
                if (typus == "V" or typus == wTag): vPlanString=vPlanString+"\n• Für diesen Tag wurde noch kein Vertretungsplan hochgeladen.";
                plain.write("• Für diesen Tag wurde noch kein Vertretungsplan hochgeladen.\n");
                
            
            if "<p><i>Leerer Vertretungsplan hochgeladen" in line.rstrip(): 
                 if (typus == "V" or typus == wTag): vPlanString=vPlanString+"\n• Keine Vertretung eingeplant.";
                 plain.write("• Keine Vertretungen eingeplant.\n");
                        
            if not '<div class="stunde"><b>Std.</b></div>' in line.rstrip():
                if '<div class="stunde">' in line.rstrip():
                    a=line.rstrip();
                    b=a.split('<div class="stunde">', 1);
                    c=b[1].split('</div>', 1);
                    Stunde=''+c[0]+''+c[1]+' ';
                    if '---' in Stunde:
                        Stunde="";
                    hatStunde=1;
                            
            if not '<div class="klasse"><b>Klasse</b></div>' in line.rstrip():
                if '<div class="klasse">' in line.rstrip():        
                    a=line.rstrip();
                    b=a.split('<div class="klasse">', 1);
                    c=b[1].split('</div>', 1);
                    Klasse=''+c[0]+''+c[1]+' ';
                    if '---' in Klasse:
                        Klasse="";
                    hatKlasse=1
                            
                            
            if not '<div class="fach"><b>Fach</b></div>' in line.rstrip():
                if '<div class="fach">' in line.rstrip():        
                    a=line.rstrip();
                    b=a.split('<div class="fach">', 1);
                    c=b[1].split('</div>', 1);
                    Fach=''+c[0]+''+c[1]+' ';
                    if '---' in Fach:
                        Fach="";
                    hatFach=1;
                            
                            
            if not '<div class="lehrer"><b>Lehrer</b></div>' in line.rstrip():
                if '<div class="lehrer">' in line.rstrip():        
                    a=line.rstrip();
                    b=a.split('<div class="lehrer">', 1);
                    c=b[1].split('</div>', 1);
                    Lehrer=''+c[0]+''+c[1]+' ';
                    if '---' in Lehrer:
                        Lehrer="";
                    hatLehrer=1;
                            

            if not '<div class="vLehrer"><b>Vertretung</b></div>' in line.rstrip():
                if '<div class="vLehrer">' in line.rstrip():        
                    a=line.rstrip();
                    b=a.split('<div class="vLehrer">', 1);
                    c=b[1].split('</div>', 1);
                    vLehrer=''+c[0]+''+c[1]+' ';
                    if '---' in vLehrer:
                        vLehrer="";
                    hatvLehrer=1;
                            
                            
            if '<div class="vFach">' in line.rstrip():        
                    a=line.rstrip();
                    b=a.split('<div class="vFach">', 1);
                    c=b[1].split('</div>', 1);
                    vFach=''+c[0]+''+c[1]+' ';
                    if '---' in vFach:
                        vFach="";
                    hatvFach=1;
                            
            if '<div class="vInfo">' in line.rstrip():        
                a=line.rstrip();
                b=a.split('<div class="vInfo">', 1);
                c=b[1].split('</div>', 1);
                Anmerkung=''+c[0]+''+c[1];
                if '---' in Anmerkung:
                    Anmerkung="";
                hatAnmerkung=1;
                            
            if(hatStunde == 1):
                if(hatKlasse == 1):
                    if(hatFach== 1):
                        if(hatLehrer == 1):
                            if(hatvLehrer == 1):
                                if(hatvFach == 1):
                                    if(hatAnmerkung == 1):
                                        res='• '+Stunde+''+Klasse+''+Fach+''+Lehrer+' -> '+vLehrer+''+vFach+'('+Anmerkung+')'
                                        
                                        if (typus == "V" or typus == wTag): vPlanString=""+vPlanString+"\n"+res
                                        plain.write(res+"\n");
                                        hatStunde=0;
                                        hatKlasse=0;
                                        hatFach=0;
                                        hatLehrer=0;
                                        hatvLehrer=0;
                                        hatvFach=0;
                                        hatAnmerkung=0;
                                        
                                        #Hier müsste dann der Kalender kommen.
                                        
                                        
        plain.close();                            
        htmlCut.close();
        return vPlanString
