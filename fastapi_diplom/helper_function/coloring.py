import networkx as nx
from helper_function import get_data, update_color, random_sorting, color_to_time

def create_lessons_dictionary(lessons_raw):
    lessons = {}

    for lesson_raw in lessons_raw:
        if lesson_raw.get('lesson_id') == None:
            continue

        lesson_id = lesson_raw.get('lesson_id')
        current_lesson = {}
        lessons[lesson_id] = current_lesson
        current_lesson['teacherIDs'] = []
        current_lesson['groupIDs'] = []
        current_lesson['classroomIDs'] = []
        current_lesson['color'] = -1
        current_lesson['chosen_classroom'] = ""
        current_lesson['nonpermitted_colors'] = lesson_raw.get('nonpermitted_colors')  
        # save the information about the teachers that must present to the dictionary
        for teacher in lesson_raw.get("teachers"):
            current_lesson['teacherIDs'].append(teacher["teacher_id"])
        # save the information about the groups of students that must present to the dictionary  
        for group in lesson_raw.get('groups'):
            current_lesson['groupIDs'].append(group["group_id"])
        # save the classrooms for this lession to the dictionary
        for classroom in lesson_raw.get('classrooms'):
            current_lesson['classroomIDs'].append(classroom["classroom_id"])       
    return lessons
#####################################################################################
def create_subjects_dictionary(lesson_raw):
    subjects = {}
    subjects["no_subject"] = []
  
    for lesson in lesson_raw:
        if lesson.get("subject_name") == "":
            subjects["no_subject"].append(lesson["lesson_id"])
        else:
            if subjects.get(lesson["subject_name"]) == None:
                subjects[lesson["subject_name"]] = {}

            current_subject = subjects[lesson["subject_name"]]
            if lesson.get("topic_name") == "":
                if current_subject.get("no_topic") == None:
                    current_subject["no_topic"] = []
                current_subject["no_topic"].append(lesson["lesson_id"])
            else:
                topic = lesson["topic_name"]
                if topic[0] < "0" or topic[0] > "9":
                    topic = "0" + topic
                if current_subject.get(topic) == None:
                    current_subject[topic] = []
                current_subject[topic].append(lesson["lesson_id"])
    return subjects
######################################################################################
def create_items_dictionary(items_raw, name):
    items = {}
    item_id = name + "_id"
    for item_raw in items_raw:
        if item_raw.get(item_id) == None:
            continue
        id = item_raw.get(item_id)
        items[id] = item_raw.get("nonpermitted_colors")
    return items

######################################################################
def create_graph(lessons, lessons_raw):
    G = nx.Graph()

    for lesson_id in lessons:
        G.add_node(lesson_id)

    for i in range(len(lessons_raw)-1):
        lesson_i = lessons_raw[i]
        if lesson_i.get('lesson_id') == None:
            continue

        teacher_id = {}
        for teacher in lesson_i["teachers"]:
            teacher_id[teacher["teacher_id"]] = True
        
        group_id = {}
        for group in lesson_i["groups"]:
            group_id[group["group_id"]] = True
        
        for j in range(i+1, len(lessons_raw)):
            lesson_j = lessons_raw[j]
            if lesson_j.get('lesson_id') == None:
                continue

            isConnected = False
            for teacher in lesson_j["teachers"]:
                if teacher_id.get(teacher["teacher_id"]):
                    G.add_edge(lesson_i["lesson_id"], lesson_j["lesson_id"])
                    isConnected = True
                    break
            if not isConnected:
                for group in lesson_j["groups"]:
                    if group_id.get(group["group_id"]):
                        G.add_edge(lesson_i["lesson_id"], lesson_j["lesson_id"])
                        isConnected = True
                        break
    return G

############################################################################################################
def set_of_nonavailable_colors(colors_not_avai, current_lesson, teachers, groups, classrooms):
    if current_lesson.get("nonpermitted_colors") != None and len(current_lesson["nonpermitted_colors"]):
        nonpermitted_colors = current_lesson["nonpermitted_colors"].split(',')
        for color in nonpermitted_colors:
            colors_not_avai.add(int(color))
    

    for teacher_id in current_lesson['teacherIDs']:
        if teachers.get(teacher_id) != None and len(teachers.get(teacher_id)):
            nonpermitted_colors = teachers[teacher_id].split(',')
            for color in nonpermitted_colors:
                colors_not_avai.add(int(color))

    for group_id in current_lesson['groupIDs']:
        if groups.get(group_id) != None and len(groups.get(group_id)):
            nonpermitted_colors = groups[group_id].split(',')
            for color in nonpermitted_colors:
                colors_not_avai.add(int(color))

    for classroom_id in current_lesson['classroomIDs']:
        if classrooms.get(classroom_id) != None and len(classrooms.get(classroom_id)):
            nonpermitted_colors = classrooms[classroom_id].split(',')
            for color in nonpermitted_colors:
                colors_not_avai.add(int(color))

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
        classroom_available[classroom["classroom_id"]] = {}

    for node in nodes:
        current_lesson = lessons[node]
        #create a set of colors that is not available for this node,
        # which contains colors of neighbor nodes and 
        # colors that the teachers that must present for this node, are not available at
        colors_not_avai = {colors[v] for v in G[node] if v in colors} 
        colors_not_avai = set_of_nonavailable_colors(colors_not_avai, current_lesson, nonavail_teachers, nonavail_groups, nonavail_classrooms)
        # find the smallest available for this node
        if dict_previous_lesson[node] == 0:
            color = 0
        else:
            color = colors[dict_previous_lesson[node]] + 1
        while True:
            # test to see if the color is in the set of unavaiable colors 
            if color not in colors_not_avai:
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
                            if classroom_available[classroom_id].get(color) == None:
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
def coloring():
    lessons_raw = get_data.get_lessons()
    classrooms = get_data.get_items("Classroom")
    teachers = get_data.get_items("Teacher")
    groups = get_data.get_items("Group")
    subjects = create_subjects_dictionary(lessons_raw)
    
    # create dictionaries with nonavailable colors for each teacher, group, classroom
    nonavail_teachers = create_items_dictionary(teachers, "teacher")
    nonavail_groups = create_items_dictionary(groups, "group")
    nonvail_classrooms = create_items_dictionary(classrooms, "classroom")

    # create lesson dictionary
    lessons = create_lessons_dictionary(lessons_raw)
    G = create_graph(lessons, lessons_raw)
    smallest_number_color = -1

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
                lessons[lesson_id]["chosen_classroom"] = chosen_classroom[lesson_id]
    return (lessons, smallest_number_color)

###############################################################################################
def update_colors_to_database():
    lessons, smallest_number_color = coloring()
    color_time = color_to_time.color_to_time(smallest_number_color)
    lesson_color_class = []
    for lesson_id in lessons:
        new_color = lessons[lesson_id]['color']
        chosen_cl = str(lessons[lesson_id]['chosen_classroom'])
        lesson_color_class.append({"lesson_id": lesson_id, "color": new_color, "chosen_classroom": chosen_cl, "time": color_time[new_color]})
    print('The smallest number of needed colors after testing 1000 times is', smallest_number_color)

    update_color.update_color(lesson_color_class)
