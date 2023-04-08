import iwe
import time
import re

'''
steps:
# turn plain text into object
# analyse query --> split up, put into categories
# go thourgh signed in users and add matches to list
# return list in text form
'''

def text_to_json(teilnehmer_liste):
    internat_pattern = r"(?<=Int\.\s).*$"
    grade_pattern = r"\((.*?)\)"
    name_pattern = r".*?(?=\s\()"

    json_list = []

    for teilnehmer in teilnehmer_liste:
        grade_and_branch = re.search(grade_pattern, teilnehmer).group(1)
        grade = grade_and_branch[0:2]
        branch = grade_and_branch[2]

        dorm_and_room = re.search(internat_pattern, teilnehmer).group().split(", ")
        dorm = dorm_and_room[0]
        room = dorm_and_room[1]

        name = re.search(name_pattern, teilnehmer).group()

        json_list.append({"name": name, "dorm": dorm, "room": room, "grade": grade, "branch": branch})

    return json_list


def get_IWE_by_query(user, password, query):
    # get students, that are signed in for IWE
    teilnehmer_liste = iwe.get_IWE({"user":user,"pwd":password})
    time.sleep(2)
    # clean users data
    teilnehmer_liste = teilnehmer_liste.split("\n\n")[1:]
    teilnehmer_liste = [teilnehmer[4:].replace('\n', ' ') for teilnehmer in teilnehmer_liste]
    teilnehmer_liste = text_to_json(teilnehmer_liste)
    
    
    queries = [query.lower() for query in re.findall(r"\w+", query)]
    
    found = []
    for teilnehmer in teilnehmer_liste:
        for query in queries:
            for value in teilnehmer.values():
                if value.lower() == query:
                    found.append(teilnehmer)
    
    found = [dict(t) for t in {tuple(student.items()) for student in found}]
    output = ["{}. {} ({}{})\nInt. {}, {}\n".format(number+1, student["name"], student["grade"], student["branch"], student["dorm"], student["room"]) for number, student in enumerate(found)]
    

    return "\n".join(output)
