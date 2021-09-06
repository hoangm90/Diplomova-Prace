import networkx as nx
import random
import json
import time

#loading data from json file
f = open('rozvrh.json',)
data = json.load(f)
f.close()

# create a dictionary with keys are ids of lessons,
# each value of the dictionary is also a new dictionary containing
# information about the teachers, the groups of students and the classroom
# for that lesson
lessons = {}

for i in range(len(data['events'])):
  if data['events'][i].get('id') == None:
    continue
  
  lessons[data['events'][i].get('id')] = {}

  lessons[data['events'][i].get('id')]['teacherIDs'] = []
  lessons[data['events'][i].get('id')]['teachers'] = []

  lessons[data['events'][i].get('id')]['groupIDs'] = []
  lessons[data['events'][i].get('id')]['groups'] = []

  lessons[data['events'][i].get('id')]['classroomIDs'] = []
  lessons[data['events'][i].get('id')]['classrooms'] = []

  # save the information about the teachers that must present to the dictionary
  for teacher in data['events'][i].get('teachersNames'):
    lessons[data['events'][i].get('id')]['teachers'].append(teacher)

  for teacherID in data['events'][i].get('teachersIds'):
    lessons[data['events'][i].get('id')]['teacherIDs'].append(teacherID)

  # save the information about the groups of students that must present to the dictionary
  for group in data['events'][i].get('groupsNames'):
    lessons[data['events'][i].get('id')]['groups'].append(group)
  
  for groupID in data['events'][i].get('groupsIds'):
    lessons[data['events'][i].get('id')]['groupIDs'].append(groupID)

  # save the classrooms for this lession to the dictionary
  for classroom in data['events'][i].get('classroomsNames'):
    lessons[data['events'][i].get('id')]['classrooms'].append(classroom)
  
  for classroomID in data['events'][i].get('classroomsIds'):
    lessons[data['events'][i].get('id')]['classroomIDs'].append(classroomID)  

# For each teacher, create the timeslots that they are not available at
teacher_not_available = {}

for i in range(len(data['teachers'])):
  teacher_not_available[data['teachers'][i]['id']] = []

random.seed(2)
for teacherId in teacher_not_available.keys():
  n = random.randint(0, 200)

  for i in range(n):
    color = random.randint(0, 10000)
    while color in teacher_not_available[teacherId]:
      color = random.randint(0, 10000)
    
    teacher_not_available[teacherId].append(color)
  
# open the file that saves the adjancent graph of lessons 
# which has been created before, and assign the graph to variable G
fh = open("test.adjlist", "rb")
G = nx.read_adjlist(fh)
fh.close()

# variable to save the smallest number of colors that needed
smallest_number_color = 0

#test the color assigning algorithm for 100 times
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
  for i in range(len(data['classrooms'])):
    classroom_available[data['classrooms'][i]['id']] = {}

  #traverse to each node and assign the smallest available color to this node 
  for u in nodes:
    #create a set of colors that is not available for this node,
    # which contains colors of neighbor nodes and 
    # colors that the teachers that must present for this node, are not available at
    colors_not_avai = {colors[v] for v in G[u] if v in colors} 
    colors_not_avai |= {color for teacherId in lessons[u]['teacherIDs'] for color in teacher_not_available[teacherId]}

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

  print("random_sequential", max_color)
  if smallest_number_color == 0 or smallest_number_color > max_color + 1:
    smallest_number_color = max_color + 1

print('The smallest number of needed colors after testing 100 times is', smallest_number_color)
