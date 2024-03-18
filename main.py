import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from IPython.display import set_matplotlib_formats
import matplotlib.patches as mpatches

set_matplotlib_formats('svg')

data = pd.read_csv("data.csv")
radius_map = {}
legend = ['food', 'shopping', 'museums', 'parks', 'monuments','hotels', 'culture', 'sports']

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
max_radius = 0
curr_max_width = 0

for location in radius_map:
  freq_list = radius_map[location]
  max_radius = max(max_radius,max(freq_list))
  if max(freq_list) > curr_max_width:
    x = x + max(freq_list) - curr_max_width
  for i in range(len(freq_list)):
    circle1 = plt.Circle((x, y), freq_list[i], color= colors_IN_ORDER[i], label ='')
    ax.add_patch(circle1)
    ax.text(x, y+max(freq_list)+1, location, ha='center', va='center', fontsize=8, style ='italic', )


  x = x + max(freq_list) *2 
  curr_max_width = max(freq_list)

ax.set_xlim(-curr_max_width, x+curr_max_width)
ax.set_ylim(-max_radius-2, max_radius+2)

# Show plot
plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')
plt.savefig('circles_plot.png')

colors_IN_ORDER = ['#342289', '#167832', '#43AA9A', '#88CCEF', '#DFCC75','#CC6577','#AA4398','#892255']

plt.legend(handles=[mpatches.Patch(color='#342289', label='Food & Drink'), 
                    mpatches.Patch(color='#167832', label='Shopping'),
                    mpatches.Patch(color='#43AA9A', label='Museums'),
                    mpatches.Patch(color='#88CCEF', label='Parks'),
                    mpatches.Patch(color='#DFCC75', label='Monuments'),
                    mpatches.Patch(color='#CC6577', label='Hotels'),
                    mpatches.Patch(color='#AA4398', label='Culture'),
                    mpatches.Patch(color='#892255', label='Sports')] 
    ,loc='lower center', 
    bbox_to_anchor=(0.5, -1.35),ncol=4, )
plt.show()