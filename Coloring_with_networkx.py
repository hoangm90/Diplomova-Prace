import json
import networkx as nx
import matplotlib.pyplot as plt

#loading data from json file
f = open('subject.json',)
data = json.load(f)
f.close()

#creating graph
G = nx.Graph()

#creating graph's nodes
for i in range(0, len(data)):
  G.add_node(data[i][0]['Subject'])

#creating graph's edges
for i in range(0, len(data) - 1):
  for j in range(i+1, len(data)):
    if data[i][1]["Teacher's name"] == data[j][1]["Teacher's name"]:
      G.add_edge(data[i][0]['Subject'], data[j][0]['Subject'])
    elif data[i][3]["Classroom"] == data[j][3]["Classroom"]:
      G.add_edge(data[i][0]['Subject'], data[j][0]['Subject'])
    else:
      for group_i in data[i][2]['Group']:
        for group_j in data[j][2]['Group']:
          if group_i == group_j:
            G.add_edge(data[i][0]['Subject'], data[j][0]['Subject'])

#using greedy algorithm to color the node
d = nx.coloring.greedy_color(G, strategy="largest_first")

#printing the names of subjects and their respective colors
for subject in d:
  print(subject, d[subject])

#drawing the graph
subax1 = plt.plot()
nx.draw(G, with_labels=True, font_weight='bold')
