import json
import networkx as nx

#loading data from json file
f = open('rozvrh.json',)
data = json.load(f)
f.close()

#creating graph
G = nx.Graph()

#creating graph's nodes
for i in range(len(data['events'])):
  if data['events'][i].get('id') == None:
    continue

  G.add_node(data['events'][i]['id'])

#creating graph's edges
for i in range(len(data['events']) - 1):
  if data['events'][i].get('id') == None:
    continue

  teacherId = {}
  for teacher in data['events'][i]['teachersIds']:
    teacherId[teacher] = True

  groupId = {}
  for group in data['events'][i]['groupsIds']:
    groupId[group] = True

  for j in range(i+1, len(data['events'])):
    if data['events'][j].get('id') == None:
      continue
     
    isConnected = False
    for teacher in data['events'][j]['teachersIds']:
      if teacherId.get(teacher) == True:
        G.add_edge(data['events'][i]['id'], data['events'][j]['id'])
        isConnected = True
        break;
    
    if not isConnected:
      for group in data['events'][j]['groupsIds']:
        if groupId.get(group) == True:
          G.add_edge(data['events'][i]['id'], data['events'][j]['id'])
          isConnected = True
          break;

# write the graph to a file
nx.write_adjlist(G, "test.adjlist")