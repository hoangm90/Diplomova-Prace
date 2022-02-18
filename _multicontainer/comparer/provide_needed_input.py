import networkx as nx
#####################################################################################
def create_subjects_dictionary(lesson_raw):
    subjects = {}
    subjects["no_subject"] = []
  
    for lesson in lesson_raw:
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
##########################################################################
def create_lessons_dictionary(lessons_raw):
    lessons = {}

    for lesson_raw in lessons_raw:
        if lesson_raw.get('id') == None:
            continue

        lesson_id = lesson_raw.get('id')
        current_lesson = {}
        lessons[lesson_id] = current_lesson
        current_lesson['teacherIDs'] = []
        current_lesson['groupIDs'] = []
        current_lesson['classroomIDs'] = []
        current_lesson['color'] = -1
        current_lesson['chosenClassroomId'] = ""
        # save the information about the teachers that must present to the dictionary
        for teacher_id in lesson_raw.get("teachersIds"):
            current_lesson['teacherIDs'].append(teacher_id)
        # save the information about the groups of students that must present to the dictionary  
        for group_id in lesson_raw.get('groupsIds'):
            current_lesson['groupIDs'].append(group_id)
        # save the classrooms for this lession to the dictionary
        for classroom_id in lesson_raw.get('classroomsIds'):
            current_lesson['classroomIDs'].append(classroom_id)     
    return lessons
######################################################################
def create_graph(lessons, lessons_raw):
    G = nx.Graph()

    for lesson_id in lessons:
        G.add_node(lesson_id)

    for i in range(len(lessons_raw)-1):
        lesson_i = lessons_raw[i]

        teachers_ids = {}
        for teacher_id in lesson_i["teachersIds"]:
            teachers_ids[teacher_id] = True
                
        groups_ids = {}
        for group_id in lesson_i["groupsIds"]:
            groups_ids[group_id] = True
                  
        for j in range(i+1, len(lessons_raw)):
            lesson_j = lessons_raw[j]

            isConnected = False
            for teacher_id in lesson_j["teachersIds"]:
                if teachers_ids.get(teacher_id):
                    G.add_edge(lesson_i["id"], lesson_j["id"])
                    isConnected = True
                    break
            if not isConnected:
                for group_id in lesson_j["groupsIds"]:
                    if groups_ids.get(group_id):
                        G.add_edge(lesson_i["id"], lesson_j["id"])
                        isConnected = True
                        break
    return G
################################################################################################
def return_needed_input(data):
    lessons_raw = data["events"]
    lessons = create_lessons_dictionary(lessons_raw)
    
    result = {}
    result["subjects"] = create_subjects_dictionary(lessons_raw)
    result["lessons"] = lessons
    result["groups"] = data["groups"]
    result["teachers"] = data["teachers"]
    result["classrooms"] = data["classrooms"]

    G = create_graph(lessons, lessons_raw)
    result["graph"] = nx.node_link_data(G)

    return result