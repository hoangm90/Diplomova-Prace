import json

#loading data from json file
f = open('subject.json',)
data = json.load(f)
f.close()

#dictionary to save degree of subject
degree_of_subject = {}

#dictionary to save subjects that connect to this subject
connect_to_subject = {}

#dictionary to save color of subject
color_of_subject = {}

#assigning initial values
for i in range(0, len(data)):
  degree_of_subject[data[i][0]['Subject']] = 0
  connect_to_subject[data[i][0]['Subject']] = []
  color_of_subject[data[i][0]['Subject']] = -1

#traversing all subject data 
for i in range(0, len(data) - 1):
  for j in range(i+1, len(data)):
    if data[i][1]["Teacher's name"] == data[j][1]["Teacher's name"]:

      #increasing degree of subject
      degree_of_subject[data[i][0]['Subject']] += 1
      degree_of_subject[data[j][0]['Subject']] += 1

      #appending subject that links to each other
      connect_to_subject[data[i][0]['Subject']].append(data[j][0]['Subject'])
      connect_to_subject[data[j][0]['Subject']].append(data[i][0]['Subject'])

    elif data[i][3]["Classroom"] == data[j][3]["Classroom"]:

      #increasing degree of subject
      degree_of_subject[data[i][0]['Subject']] += 1
      degree_of_subject[data[j][0]['Subject']] += 1

      #appending subject that links to each other
      connect_to_subject[data[i][0]['Subject']].append(data[j][0]['Subject'])
      connect_to_subject[data[j][0]['Subject']].append(data[i][0]['Subject'])

    else:
      for group_i in data[i][2]['Group']:
        for group_j in data[j][2]['Group']:
          if group_i == group_j:

            #increasing degree of subject
            degree_of_subject[data[i][0]['Subject']] += 1
            degree_of_subject[data[j][0]['Subject']] += 1

            #appending subject that links to each other
            connect_to_subject[data[i][0]['Subject']].append(data[j][0]['Subject'])
            connect_to_subject[data[j][0]['Subject']].append(data[i][0]['Subject'])

#sorting subjects according to their degree
degree_of_subject = sorted(degree_of_subject.items(), key=lambda x: x[1], reverse=True)
sorted_subject = []
for subject in degree_of_subject:
  sorted_subject.append(subject[0])

#assigning color to subjects
for subject in sorted_subject:
  color = 0
  while color_of_subject[subject] == -1:
    can_use_this_color = True

    #checking if the color is used by subject's neighbor
    for neighbor in connect_to_subject[subject]:
      if color_of_subject[neighbor] == color:
        color += 1
        can_use_this_color = False
        break

    #assigning the color to the subject if the color is not used yet
    if can_use_this_color:
      color_of_subject[subject] = color

#printing out the subjects and their colors
for subject in color_of_subject:
  print(subject, color_of_subject[subject])
