import numpy as np
import matplotlib.pyplot as plt

N = 9
ind = np.arange(N)  # the x locations for the groups
width = 3     # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)

Tanimoto = [0.39,0.36,0.32,0.35,0.33]
rects1 = ax.bar([1, 11, 21, 31,41], Tanimoto, width, color='w')

Forbes = [0.20,0.30,0.47,0.25,0.25]
rects2 = ax.bar([4,14,24,34,44], Forbes, width, hatch = '////', color='w')

GP = [0.28,0.45,0.45,0.44,0.44]
rects3 = ax.bar([7, 17, 27,37,47], GP, width, hatch = '*****', color='w')

# add some text for labels, title and axes ticks
ax.set_ylabel('Fitness Value')
ax.set_title('Fitness Function All Class')
ax.set_xticks([5.5, 15.5, 25.5, 35.5, 45.5])
ax.set_xticklabels(('Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5'))

ax.legend((rects1[0], rects2[0], rects3[0]),
          ('Tanimoto', 'Forbes', 'GP'), ncol=3)

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2.0, h, '%d'%int(h),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.ylim(0, 1)
plt.xlim(0, 52)


plt.show()

N = 9
ind = np.arange(N)  # the x locations for the groups
width = 3     # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)

Tanimoto = [90,93,90,95,91]
rects1 = ax.bar([1, 11, 21, 31,41], Tanimoto, width, color='w')

Forbes = [89,80,88,85,81]
rects2 = ax.bar([4,14,24,34,44], Forbes, width, hatch = '////', color='w')

GP = [89,83,82,80,81]
rects3 = ax.bar([7, 17, 27,37,47], GP, width, hatch = '*****', color='w')

# add some text for labels, title and axes ticks
ax.set_ylabel('Accuracy (%)')
ax.set_title('Accuracy for All Class')
ax.set_xticks([5.5, 15.5, 25.5, 35.5, 45.5])
ax.set_xticklabels(('Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5'))

ax.legend((rects1[0], rects2[0], rects3[0]),
          ('Tanimoto', 'Forbes', 'GP'), ncol=3)

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2.0, 0.1+h, '%d'%int(h),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.ylim(0, 120)
plt.xlim(0, 52)


plt.show()