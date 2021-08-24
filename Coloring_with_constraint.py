import json

#using recursive backtrack to assign color to node with constraint
def coloring(index, sorted_subject, connect_to_subject, color_of_subject, constraint_color):
#Base case: the last subject that need to be assigned color
  if index == len(sorted_subject) -1:
    #check what color can be used for this subject
    for color in constraint_color[sorted_subject[index]]:
      can_use_color = True
      for neighbor in connect_to_subject[sorted_subject[index]]:
        if color_of_subject[neighbor] == color:
          can_use_color = False
          break

      #if there is valid color, assigning it to the subjec and return true
      if can_use_color:
        color_of_subject[sorted_subject[index]] = color
        return True
    
    #return false if there is no valid color
    return False
  
#recursive case: assigning valid color to a node and then come to the next node
  #t is the variable to check whether it is possible to 
  #assign color to this node, and all the nodes after it in the list
  t = False 
  for color in constraint_color[sorted_subject[index]]:
    #checking if the color is valid or not
    can_use_color = True
    for neighbor in connect_to_subject[sorted_subject[index]]:
      if color_of_subject[neighbor] == color:
        can_use_color = False
        break

    #if the color is valid, assigning it to the node and come to the next one
    if can_use_color:
      color_of_subject[sorted_subject[index]] = color
      t = coloring(index+1, sorted_subject, connect_to_subject, color_of_subject, constraint_color)
      if t:
        return t

  return t

def main():
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

  constraint_color = {}

  #assign initial values
  for i in range(0, len(data)):
    degree_of_subject[data[i][0]['Subject']] = 0
    connect_to_subject[data[i][0]['Subject']] = []
    color_of_subject[data[i][0]['Subject']] = -1
    constraint_color[data[i][0]['Subject']] = data[i][4]['Constraint']

  #traverse all subject data 
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
  degree_of_subject = sorted(degree_of_subject)

  #assigning subject to list of subjects according to their degree
  sorted_subject = []
  for subject in degree_of_subject:
    sorted_subject.append(subject)

  #assigning color to subject
  t = coloring(0, sorted_subject, connect_to_subject, color_of_subject, constraint_color)

  #printing subjects and their colors
  if t:
    for subject in color_of_subject:
      print(subject, color_of_subject[subject])
  else:
    print('False')

if __name__ == '__main__':
  main()