import urllib.request
import json
import networkx as nx
import time
import random

try:
   with urllib.request.urlopen('http://127.0.0.1:8000/lessons') as f:
      data = f.read().decode('utf8')
except urllib.error.URLError as e:
   print(e.reason)

lesson_raw = json.loads(data)

try:
   with urllib.request.urlopen('http://127.0.0.1:8000/classrooms') as f:
      data = f.read().decode('utf8')
except urllib.error.URLError as e:
   print(e.reason)

classrooms = json.loads(data)

lessons = {}

for i in range(len(lesson_raw)):
    if lesson_raw[i].get('lesson_id') == None:
        continue
  
    lesson_id = lesson_raw[i].get('lesson_id')
    lessons[lesson_id] = {}

    lessons[lesson_id]['teacherIDs'] = []

    lessons[lesson_id]['groupIDs'] = []

    lessons[lesson_id]['classroomIDs'] = []
    
    # save the information about the teachers that must present to the dictionary
    for teacher in lesson_raw[i].get("teachers"):
        lessons[lesson_id]['teacherIDs'].append(teacher["teacher_id"])

    # save the information about the groups of students that must present to the dictionary  
    for group in lesson_raw[i].get('groups'):
        lessons[lesson_id]['groupIDs'].append(group["group_id"])

    # save the classrooms for this lession to the dictionary
    for classroom in lesson_raw[i].get('classrooms'):
        lessons[lesson_id]['classroomIDs'].append(classroom["classroom_id"])  

G = nx.Graph()

for lesson_id in lessons:
    G.add_node(lesson_id)

for i in range(len(lesson_raw)-1):
    if lesson_raw[i].get('lesson_id') == None:
        continue

    teacher_id = {}
    for teacher in lesson_raw[i]["teachers"]:
        teacher_id[teacher["teacher_id"]] = True
    
    group_id = {}
    for group in lesson_raw[i]["groups"]:
        group_id[group["group_id"]] = True
    
    for j in range(i+1, len(lesson_raw)):
        if lesson_raw[j].get('lesson_id') == None:
            continue

        isConnected = False
        for teacher in lesson_raw[j]["teachers"]:
            if teacher_id.get(teacher["teacher_id"]):
                G.add_edge(lesson_raw[i]["lesson_id"], lesson_raw[j]["lesson_id"])
                isConnected = True
                break
        if not isConnected:
            for group in lesson_raw[j]["groups"]:
                if group_id.get(group["group_id"]):
                    G.add_edge(lesson_raw[i]["lesson_id"], lesson_raw[j]["lesson_id"])
                    isConnected = True
                    break

smallest_number_color = 0

for k in range(100):
    # The first test will be coloring nodes in the order of degree
    # color the node with largest degree first, and the node with smallest degree last
    # this is the most common strategy for ordering nodes
    if k == 0:
        nodes = sorted(G, key=G.degree, reverse=True)
    else:
    # order the node randomly to assure that the algorithm is stochastic
        t = 1000 * time.time() # current time in milliseconds
        random.seed(int(t) % 2**32)
        nodes = list(G)
        random.shuffle(nodes)

    # create the dictionary with keys are lessons
    # and values are color assigning to each lesson
    colors = {}
    
    # create a dictionary to track if a classroom is available
    # in a specific timeslots
    classroom_available = {}
    for i in range(len(classrooms)):
        classroom_available[classrooms[i]["classroom_id"]] = {}

    #traverse to each node and assign the smallest available color to this node 
    for u in nodes:
        #create a set of colors that is not available for this node,
        # which contains colors of neighbor nodes and 
        # colors that the teachers that must present for this node, are not available at
        colors_not_avai = {colors[v] for v in G[u] if v in colors} 

        # find the smallest available for this node
        color = 0
        while True:
            # test to see if the color is in the set of unavaiable colors 
            if color not in colors_not_avai:
                # if the color is not in the set, then test to see if 
                # there is available room for this lesson at this color(timeslot)
                if len(lessons[u]['classroomIDs']) == 0:
                    break
                else:
                    can_assign_classroom = False
                    for classroom in lessons[u]['classroomIDs']:
                        if classroom_available[classroom].get(color) == None:
                        # if the is available room, assign that room to this lesson and break the loop
                            classroom_available[classroom][color] = True
                            can_assign_classroom = True
                            break

                    if can_assign_classroom:
                        break
            # if the considered color is not available, raise it for 1 
            color += 1

        # assign the available color(timeslot) to the node(lession)
        colors[u] = color

    # find the biggest assigned color, which indicates how many colors(timeslots)
    # are needed for this time table
    max_color = 0
    for lesson in colors:
        if colors[lesson] > max_color:
            max_color = colors[lesson]

    print("random_sequential", max_color, colors)
    if smallest_number_color == 0 or smallest_number_color > max_color + 1:
        smallest_number_color = max_color + 1

print('The smallest number of needed colors after testing 100 times is', smallest_number_color)