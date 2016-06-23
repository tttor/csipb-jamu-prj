import numpy as np
import matplotlib.pyplot as plt

N = 9
ind = np.arange(N)  # the x locations for the groups
width = 3     # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)

KNN = [89.22,86.82,86.82,85.33,83.84]
rects1 = ax.bar([1, 11, 21, 31,41], KNN, width, color='#1abc9c')

KNN_Tanimoto = [90.43,90.42,87.73,85.93,85.93]
rects2 = ax.bar([4,14,24,34,44], KNN_Tanimoto, width, color='#f1c40f')

KNN_GP = [88.32,85.92,85.33,84.74,84.44]
rects3 = ax.bar([7, 17, 27,37,47], KNN_GP, width, color='#3498db')

# add some text for labels, title and axes ticks
ax.set_ylabel('Akurasi (%)')
ax.set_title('Uji KNN')
ax.set_xticks([5.5, 15.5, 25.5, 35.5, 45.5])
ax.set_xticklabels(('n = 3', 'n = 5', 'n = 7', 'n = 9', 'n = 11'))

ax.legend((rects1[0], rects2[0], rects3[0]),
          ('KNN', 'KNN-Tanimoto', 'KNN-GP'), ncol=3)

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2.0, 1.05*h, '%d'%int(h),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.ylim(0, 120)
plt.xlim(0, 52)


plt.show()