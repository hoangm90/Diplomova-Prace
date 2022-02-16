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
        current_lesson['nonpermittedColors'] = []
        # save the information about the teachers that must present to the dictionary
        for teacher_id in lesson_raw.get("teachersIds"):
            current_lesson['teacherIDs'].append(teacher_id)
        # save the information about the groups of students that must present to the dictionary  
        for group_id in lesson_raw.get('groupsIds'):
            current_lesson['groupIDs'].append(group_id)
        # save the classrooms for this lession to the dictionary
        for classroom_id in lesson_raw.get('classroomsIds'):
            current_lesson['classroomIDs'].append(classroom_id)     
        # save nonpermitted time intervals 
        if lesson_raw.get('nonpermittedTimes') != None:
            for nonper_time in lesson_raw.get('nonpermittedTimes'):
                nonper_color = color_time.time_to_color(nonper_time)
                current_lesson['nonpermittedColors'].append(nonper_color)
    return lessons

def sort_helper(e):
    num = 0
    i = 0
    while e[i] >= "0" and e[i] <= "9":
        num = num*10 + int(e[i])
        i+=1
    return num

def divide_data(lesson_raw):
    subjects = create_subjects_dictionary(lesson_raw)
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
    
    lesson_ids1 = []
    lesson_ids2 = []
    ls_helper=[]
    for i in range(len(ls)):
        n = len(ls[i])//2
        for j in range(n):
            lesson_ids1.append(ls[i][j])
        for j in range(n, len(ls[i])):
            lesson_ids2.append(ls[i][j])
        for j in range(len(ls[i])):
            ls_helper.append(ls[i][j])
    
    lessons = create_lessons_dictionary(lesson_raw)
    lessons1 = {}
    lessons2 = {}
    for lesson_id in lesson_ids1:
        lessons1[lesson_id] = lessons[lesson_id]   
    for lesson_id in lesson_ids2:
        lessons2[lesson_id] = lessons[lesson_id]
    
    lessons_raw1 = []
    lessons_raw2 = []
    for lesson in lesson_raw:
        if lesson.get("id") == None:
            continue
        if lessons1.get(lesson["id"]):
            lessons_raw1.append(lesson)
        else:
            lessons_raw2.append(lesson)
    return lessons1, lessons_raw1, lessons2, lessons_raw2