import time as waitTime
from time import time as utc_time
from datetime import datetime, time
import re
import requests
import codecs
import manUsers

def appr(url, payload):
    with requests.Session() as s:  
        r = s.post(url, data=payload);
        waitTime.sleep(1)
        cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}                                      #Friss den Cookie                                                                                                 
        r = s.post('https://www.landesschule-pforta.de/intern/aktuell/vertretungsplan.php', cookies=cookie, data=payload)       #Nutze cookie, um HiddenSite zu öffnen
        waitTime.sleep(1)
        htmlContents = r.text
        name=""
        try:
            cutClass=htmlContents.split("Angemeldet:", 1);
            return true
        except IndexError:
            return false
        except:
            pass