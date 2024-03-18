import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')

data = pd.read_csv("data.csv")
radius_map = {}
category_to_row = {'food':0, 'shopping':1, 'museums':2, 'parks':3, 'monuments':4,'hotels':5, 'culture':6, 'sports':7}
for index, row in data.iterrows():
  location = row['location']
  category = row['category']
  if location in radius_map:
    index = category_to_row[category]
    radius_map[location][index] = radius_map[location][index] + 1
  else:
    radius_map[location] = [0,0,0,0,0,0,0,0]
    index = category_to_row[category]
    radius_map[location][index] = 1

for location in radius_map:
  freq_list = radius_map[location]
  #iterating backwards and updating the values
  for i in range(len(freq_list) - 2, -1, -1):
    freq_list[i] = freq_list[i] + freq_list[i+1]
colors_IN_ORDER = ['#342289', '#167832', '#43AA9A', '#88CCEF', '#DFCC75','#CC6577','#AA4398','#892255']
fig, ax = plt.subplots()


x,y = 0,0
for location in radius_map:
  freq_list = radius_map[location]
  for i in range(len(freq_list)):
    #plt.scatter(x, y, color = colors_IN_ORDER[i], marker = 'o', s = freq_list[i]*1000)
    circle1 = plt.Circle((x, y), freq_list[i], color= colors_IN_ORDER[i])
    ax.add_patch(circle1)
  x = x + max(freq_list) *2

ax.set_xlim(0, 100)
ax.set_ylim(-100, 100)

# Show plot
plt.gca().set_aspect('equal', adjustable='box')
#plt.axis('off')
plt.savefig('circles_plot.png')
plt.show()