import networkx as nx
import json
import random_sorting, color_time

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
#####################################################################################
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
######################################################################################
def create_nonavail_items_dictionary(items_raw):
    nonavail_items = {}
    for item in items_raw:
        if item.get("id") == None:
            continue
        id = item["id"]
        nonavail_item = {}
        nonpermitted_times = item.get('nonpermittedTimes')
        if nonpermitted_times != None:
            for nonper_time in nonpermitted_times:
                nonper_color = color_time.time_to_color(nonper_time)
                nonavail_item[nonper_color] = True
        nonavail_items[id] = nonavail_item
    return nonavail_items

######################################################################
def create_graph(lessons, lessons_raw):
    G = nx.Graph()

    for lesson_id in lessons:
        G.add_node(lesson_id)

    for i in range(len(lessons_raw)-1):
        lesson_i = lessons_raw[i]
        if lesson_i.get('id') == None:
            continue

        teachers_ids = {}
        for teacher_id in lesson_i["teachersIds"]:
            teachers_ids[teacher_id] = True
        
        groups_ids = {}
        for group_id in lesson_i["groupsIds"]:
            groups_ids[group_id] = True
        
        for j in range(i+1, len(lessons_raw)):
            lesson_j = lessons_raw[j]
            if lesson_j.get('id') == None:
                continue

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

############################################################################################################
def set_of_nonavailable_colors(colors_not_avai, current_lesson):
    for nonper_color in current_lesson["nonpermittedColors"]:
        colors_not_avai.add(nonper_color)
    return colors_not_avai
    
#############################################################################################################
def coloring_helper(subjects, lessons, classrooms, nonavail_teachers, nonavail_groups, nonavail_classrooms, G):
    [nodes, dict_previous_lesson] = random_sorting.random_sorting(subjects)
    # create the dictionary with keys are lessons
    # and values are color assigning to each lesson,
    # and classroom assigning to each lesson
    colors = {}
    chosen_classroom = {}
    
    # create a dictionary to track if a classroom is available
    # in a specific timeslots
    classroom_available = {}
    for classroom in classrooms:
        classroom_available[classroom["id"]] = {}

    for node in nodes:
        current_lesson = lessons[node]
        #create a set of colors that is not available for this node,
        # which contains colors of neighbor nodes and 
        # colors that the teachers that must present for this node, are not available at
        colors_not_avai = {colors[v] for v in G[node] if v in colors} 
        colors_not_avai = set_of_nonavailable_colors(colors_not_avai, current_lesson)
        # find the smallest available for this node
        if dict_previous_lesson[node] == 0:
            color = 0
        else:
            color = colors[dict_previous_lesson[node]] + 1
        while True:
            # test to see if the color is in the set of unavaiable colors 
            if color not in colors_not_avai:
                can_assign = True
                # if the teachers are available at this color
                for teacher_id in current_lesson['teacherIDs']:
                    if nonavail_teachers[teacher_id].get(color):
                        can_assign = False
                        break
                if not can_assign:
                    color += 1
                    continue
                # if the groups are available at this color
                for group_id in current_lesson['groupIDs']:
                    if nonavail_groups[group_id].get(color):
                        can_assign = False
                        break
                if not can_assign:
                    color += 1
                    continue
                # if the color is not in the set, then test to see if 
                # there is available room for this lesson at this color(timeslot)
                if len(current_lesson['classroomIDs']) == 0:
                    chosen_classroom[node] = ""
                    break
                else:
                    can_assign_classroom = False
                    for classroom_id in current_lesson['classroomIDs']:
                        if classroom_id == 1280 or classroom_id == 1281 or classroom_id == 1284:
                            chosen_classroom[node] = classroom_id
                            can_assign_classroom = True
                    if can_assign_classroom == False:
                        for classroom_id in current_lesson['classroomIDs']:
                            if classroom_available[classroom_id].get(color) == None and nonavail_classrooms[classroom_id].get(color) == None:
                            # if the is available room, assign that room to this lesson and break the loop
                                classroom_available[classroom_id][color] = True
                                chosen_classroom[node] = classroom_id
                                can_assign_classroom = True
                                break

                    if can_assign_classroom:
                        break
                # if the considered color is not available, raise it for 1 
            color += 1
        # assign the available color(timeslot) to the node(lession)
        colors[node] = color
    
    return (colors, chosen_classroom)

#############################################################################################
def find_max_color(colors):
    max_color = 0
    for lesson in colors:
        if colors[lesson] > max_color:
            max_color = colors[lesson]
    return max_color

############################################################################################
def coloring(data):
    lessons_raw = data["events"]
    classrooms = data["classrooms"]
    teachers = data["teachers"]
    groups = data["groups"]
    subjects = create_subjects_dictionary(lessons_raw)
    
    # create dictionaries with nonavailable colors for each teacher, group, classroom
    nonavail_teachers = create_nonavail_items_dictionary(teachers)
    nonavail_groups = create_nonavail_items_dictionary(groups)
    nonvail_classrooms = create_nonavail_items_dictionary(classrooms)

    # create lesson dictionary
    lessons = create_lessons_dictionary(lessons_raw)
    G = create_graph(lessons, lessons_raw)
    smallest_number_color = -1

    dict_classrooms = {}
    for cl in classrooms:
        dict_classrooms[cl["id"]] = cl["name"]

    for k in range(100):
        colors, chosen_classroom = coloring_helper(subjects, lessons, classrooms, nonavail_teachers, nonavail_groups, nonvail_classrooms, G)
        # find the biggest assigned color, which indicates how many colors(timeslots)
        # are needed for this time table
        max_color = find_max_color(colors)       
        # if number of colors using in the new variant is smaller, take the result instead of the old one
        if smallest_number_color == -1 or smallest_number_color >= max_color + 1:
            smallest_number_color = max_color + 1
            for lesson_id in colors:
                lessons[lesson_id]['color'] = colors[lesson_id]
            for lesson_id in chosen_classroom:
                lessons[lesson_id]["chosenClassroomId"] = chosen_classroom[lesson_id]
                lessons[lesson_id]["chosenClassroom"] = dict_classrooms.get(chosen_classroom[lesson_id]) if dict_classrooms.get(chosen_classroom[lesson_id]) != None else ""

    return (lessons, smallest_number_color)

###############################################################################################
def sort_lessons(lessons_raw):
    colors = []
    max_color = -1
    for lesson in lessons_raw:
        if lesson['color'] > max_color:
            max_color = lesson['color']
    
    for i in range(max_color + 1):
        colors.append([])
    
    for lesson in lessons_raw:
        colors[lesson['color']].append(lesson)

    return colors

################################################################################################
def return_planned_timetables(raw_data: bytes):
    data = json.loads(raw_data)
    lessons, smallest_number_color = coloring(data)
    color_to_time = color_time.color_to_time(smallest_number_color)

    dict_classrooms = {}
    for cl in data["classrooms"]:
        dict_classrooms[cl["id"]] = cl["name"]

    lessons_raw = data["events"]
    for l in lessons_raw:
        id = l["id"]
        l["color"] = lessons[id]["color"]
        l["chosenClassroomId"] = lessons[id]["chosenClassroomId"]
        l["chosenClassroom"] = dict_classrooms.get(l["chosenClassroomId"]) if dict_classrooms.get(l["chosenClassroomId"]) != None else ""
        l["occurringTime"] = color_to_time[l["color"]]
    print('The smallest number of needed colors after testing 100 times is', smallest_number_color)
    result = {}
    result['events'] = sort_lessons(lessons_raw)
    result["teachers"] = data["teachers"]
    result["groups"] = data["groups"]
    result["classrooms"] = data["classrooms"]
    return result
