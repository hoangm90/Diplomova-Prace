import color_time

def create_subjects_dictionary(lesson_raw):
    subjects = {}
    subjects["no_subject"] = []
  
    for lesson in lesson_raw:
        if lesson.get('id') == None:
            continue
        if lesson.get("subjectName") == None:
            subjects["no_subject"].append(lesson["id"])
        else:
            if subjects.get(lesson["subjectName"]) == None:
                subjects[lesson["subjectName"]] = {}

            current_subject = subjects[lesson["subjectName"]]
            if lesson.get("topic") == None:
                if current_subject.get("no_topic") == None:
                    current_subject["no_topic"] = []
                current_subject["no_topic"].append(lesson["id"])
            else:
                topic = lesson["topic"]
                if topic[0] < "0" or topic[0] > "9":
                    topic = "0" + topic
                if current_subject.get(topic) == None:
                    current_subject[topic] = []
                current_subject[topic].append(lesson["id"])
    return subjects
##########################################################################################################
def sort_helper(e):
    num = 0
    i = 0
    while e[i] >= "0" and e[i] <= "9":
        num = num*10 + int(e[i])
        i+=1
    return num
###########################################################################################################
def divide_data(data):
    lessons_raw = data["events"]
    subjects = create_subjects_dictionary(lessons_raw)
    ls = []
    ls.append([])
    for lesson in subjects["no_subject"]:
        ls[0].append(lesson)
    i=1
    for sub in subjects:
        if sub == "no_subject":
            continue
        else:
            ls.append([])
            topic_list = []
            for topic in subjects[sub]:
                topic_list.append(topic)
            topic_list.sort(key=sort_helper)
      
            for tp in topic_list:
                for lesson in subjects[sub][tp]:
                    ls[i].append(lesson)
            i += 1
    
    lesson_ids1 = {}
    lesson_ids2 = {}
    for i in range(len(ls)):
        n = len(ls[i])//2
        for j in range(n):
            lesson_ids1[ls[i][j]] = True
        for j in range(n, len(ls[i])):
            lesson_ids2[ls[i][j]] = True
    
    lessons_raw1 = []
    lessons_raw2 = []
    for lesson in lessons_raw:
        if lesson.get("id") == None:
            continue
        if lesson_ids1.get(lesson["id"]):
            lessons_raw1.append(lesson)
        else:
            lessons_raw2.append(lesson)

    input1 = {}
    input1["events"] = lessons_raw1
    input1["groups"] = data["groups"]
    input1["teachers"] = data["teachers"]
    input1["classrooms"] = data["classrooms"]
    input1["order"] = 1

    input2 = {}
    input2["events"] = lessons_raw2
    input2["groups"] = data["groups"]
    input2["teachers"] = data["teachers"]
    input2["classrooms"] = data["classrooms"]
    input2["order"] = 2

    return [input1, input2]