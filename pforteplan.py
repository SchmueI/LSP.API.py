from datetime import datetime,timedelta
import vplan
import manUsers
import mealInfo
import agInfo

def generate_plan():
    """
    Collect all Strings and Send them
    """
    weekdays=["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
    shift = datetime.now() + timedelta(days=1)
    tomorrow = str(weekdays[shift.weekday()]) + ", " + shift.strftime('%d.%m.%Y')
    vplanDay=str(weekdays[shift.weekday()])
    
    msg="<b>"+tomorrow+"</b>\n\n"
    if not (vplanDay == "Samstag" or vplanDay == "Sonntag"):msg="<b>"+tomorrow+"</b>\n\n<u>Vertretungsplan</u>"
    if not (vplanDay == "Samstag" or vplanDay == "Sonntag"):msg=msg+vplan.get_plan('https://www.landesschule-pforta.de/login.php', {'user':manUsers.show(uID, "username"), 'pwd':manUsers.show(uID, "password")}, uID, vplanDay)+"\n\n"
    msg=msg+"<u>Essen</u>"+mealInfo.plan(str(weekdays[shift.weekday()]))+"\n"
    msg=msg+"<u>Arbeitsgruppen (AGs)</u>"+agInfo.plan(str(weekdays[shift.weekday()]))+"\n"
    msg=msg+"<u>Essensausgabezeiten</u>"+mealInfo.time+"\n\n"
    
    return msg
