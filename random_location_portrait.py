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
max_radii_for_location = []
for location in radius_map:
  freq_list = radius_map[location]
  max_radii = 0
  #iterating backwards and updating the values
  for i in range(len(freq_list) - 2, -1, -1):
    freq_list[i] = freq_list[i] + freq_list[i+1]
    max_radii = max(max_radii, freq_list[i])
  max_radii_for_location.append(max_radii)
colors_IN_ORDER = ['#342289', '#167832', '#43AA9A', '#88CCEF', '#DFCC75','#CC6577','#AA4398','#892255']

current_circles = []  
for i in range(len(radius_map)):
    while len(current_circles) < len(radius_map):
        x = np.random.uniform(-sum(max_radii_for_location)/2 , sum(max_radii_for_location)/2)
        y = np.random.uniform(-sum(max_radii_for_location)/2 , sum(max_radii_for_location)/2)
        collide = False
        for x2, y2, r2 in current_circles:
            d = np.sqrt((x - x2)**2 + (y - y2)**2)
            if d < max_radii_for_location[i] + r2:
                collide = True
                break
        if not collide:
            current_circles.append((x, y, max_radii_for_location[i]))
            break

fig, ax = plt.subplots()
index = 0
max_radius = 0
curr_max_width = 0

for location in radius_map:
  freq_list = radius_map[location]
  max_radius = max(max_radius,max(freq_list))
  for i in range(len(freq_list)):
    x,y,r = current_circles[index]
    circle1 = plt.Circle((x, y), freq_list[i], color= colors_IN_ORDER[i], label ='')
    ax.add_patch(circle1)
    ax.text(x, y+max(freq_list)+1, location, ha='center', va='center', fontsize=8, style ='italic', )
  curr_max_width = max(freq_list)
  index = index + 1
left_bound = 0
up_bound = 0
right_bound = 0
down_bound = 0
for circle in current_circles:
   x,y,r = circle
   if x + r > right_bound:
      right_bound = x + r
   if x - r < left_bound:
      left_bound = x - r

   if y + r > up_bound:
      up_bound = y + r
   if y - r < down_bound:
      down_bound = y - r

ax.set_xlim(left_bound-2, right_bound+10)
ax.set_ylim(down_bound-10, up_bound+2)
plt.axis('off')

plt.gca().set_aspect('equal', adjustable='box')
plt.legend(handles=[mpatches.Patch(color='#342289', label='Food & Drink'), 
                    mpatches.Patch(color='#167832', label='Shopping'),
                    mpatches.Patch(color='#43AA9A', label='Museums'),
                    mpatches.Patch(color='#88CCEF', label='Parks'),
                    mpatches.Patch(color='#DFCC75', label='Monuments'),
                    mpatches.Patch(color='#CC6577', label='Hotels'),
                    mpatches.Patch(color='#AA4398', label='Culture'),
                    mpatches.Patch(color='#892255', label='Sports')] ,loc='best',bbox_to_anchor=(0.5, 0., 0.5, 0.5), ncols=2)
plt.show()
