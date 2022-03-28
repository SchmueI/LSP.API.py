import time as waitTime
from time import time as utc_time
from datetime import datetime, time
import re
import requests
import codecs

def registrations(payload):

    with requests.Session() as s:
        r = s.post("https://www.landesschule-pforta.de/login.php", data=payload);
        cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}
        waitTime.sleep(1)
        r = s.post('https://www.landesschule-pforta.de/intern/aktuell/busreservierung.php', cookies=cookie, data=payload)
        waitTime.sleep(1)
        content = r.text
        retValue = ""
        if ("<h1>Busreservierung</h1>" in content):
            content = content.split("reservierung</h1>", 1)[1]
            if ("In der Datenbank sind keine Abreisetage registriert." in content): return ""
            content = content.split("Nmb (12:50)</b></div>", 1)[1]
            retValue = "<b>Bus nach Naumburg (12:50)</b>"
            retValue = retValue + content.split('<div class="busRe">', 1)[0].replace("<div>", "").replace("</div>", "").replace("	", "")
            content = content.split('<div class="busRe">', 1)[1]
            content = content.split('BK (12:50)</b></div>', 1)[1]
            retValue = retValue + "<b>Bus nach Bad Kösen (12:50)</b>"
            retValue = retValue + content.split('<!-- Ende Inhalt -->', 1)[0].replace("<div>", "").replace("</div>", "").replace("	", "")
            if ('<div class="top18 abstand4"><b>... mit Wechseloption zum Bus nach Nmb</b>' in retValue): 
                retValue = retValue.replace('<div class="top18 abstand4"><b>... mit Wechseloption zum Bus nach Nmb</b>', '\n<b>Mit wechseloption zum Bus nach Nmb</b>')
            if ('<div class="rot">' in retValue):
                retValue = retValue.replace('<div class="rot">', '')
            return retValue
        else: 
            return "Konnte keine Verbindung zum Server herstellen.\nDas kann zum Beispiel an zu vielen Zugriffen liegen. Probiere später nochmal /rplan um die bisherigen Anmeldungen zu sehen."

def register(wsuser, wspass, wskind):
    with requests.Session() as s:
        r = s.post("https://www.landesschule-pforta.de/login.php", data={'user':wsuser ,'pwd':wspass});
        cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}
        r = s.post('https://www.landesschule-pforta.de/intern/aktuell/busreservierung.php', cookies=cookie, data={'user':wsuser ,'pwd':wspass})          
        if(wskind==0):
            r = s.post('https://www.landesschule-pforta.de/intern/aktuell/busreservierung.php', cookies=cookie, data={'user':wsuser, 'pwd':wspass, 'aktion':'', 'aktion':'reservierungSpeichern', 'bus':'0'}) 
            waitTime.sleep(1)
            if not (registrations("https://www.landesschule-pforta.de/login.php", {"user":wsuser,"pwd":wspass})==""): return 1
            else: return 0
        elif(wskind==1):
            r = s.post('https://www.landesschule-pforta.de/intern/aktuell/busreservierung.php', cookies=cookie, data={'user':wsuser, 'pwd':wspass, 'aktion':'', 'aktion':'reservierungSpeichern', 'bus':'1'})
            waitTime.sleep(1)
            if not (registrations("https://www.landesschule-pforta.de/login.php", {"user":wsuser,"pwd":wspass})==""): return 1
            else: return 0
        else:
            r = s.post('https://www.landesschule-pforta.de/intern/aktuell/busreservierung.php', cookies=cookie, data={'user':wsuser, 'pwd':wspass, 'aktion':'', 'aktion':'reservierungSpeichern', 'bus':'2'}) 
            waitTime.sleep(1)
            if not (registrations("https://www.landesschule-pforta.de/login.php", {"user":wsuser,"pwd":wspass})==""): return 1
            else: return 0

def deregister(wsuser, wspass):

    with requests.Session() as s:
        r = s.post("https://www.landesschule-pforta.de/login.php", data={'user':wsuser ,'pwd':wspass});
        cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}
        r = s.post('https://www.landesschule-pforta.de/intern/aktuell/iweAnmeldung.php', cookies=cookie, data={'user':wsuser ,'pwd':wspass})
        r = s.post('https://www.landesschule-pforta.de/intern/aktuell/busreservierung.php', cookies=cookie, data={'user':wsuser, 'pwd':wspass, 'aktion':'', 'aktion':'reservierungLoeschen'}) 
        waitTime.sleep(1)
        return 1
