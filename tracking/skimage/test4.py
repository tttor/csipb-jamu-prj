#!/usr/bin/python
from skimage import io
from skimage import data
from skimage import filters
from skimage import measure
from skimage.color import rgb2gray
from skimage.segmentation import clear_border
from skimage.segmentation import mark_boundaries
from skimage.morphology import watershed
from skimage.feature import peak_local_max

from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np

# img_filepath = '/home/tor/robotics/prj/uq-cell-prj/ws/circular-extract/cell.png'
# img_rgb = io.imread(img_filepath)
# img_gray = rgb2gray(img_rgb)
img_gray = data.coins()

# OTSU
mask = img_gray > filters.threshold_otsu(img_gray)
clean_border = clear_border(mask)

# WATERSHED
distance = ndimage.distance_transform_edt(img_gray)
local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)),labels=img_gray)
markers = measure.label(local_maxi)
labels_ws = watershed(-distance, markers, mask=img_gray)


#
# plt.figure()
# plt.imshow(clean_border, cmap='gray')

# plt.figure()
# plt.imshow(img_gray, cmap='gray')
# plt.contour(clean_border, [0.5])

# coins_edges = mark_boundaries(img_gray, clean_border)
# plt.imshow(coins_edges)

# edges = mark_boundaries(img_gray, clean_border)
# plt.imshow(edges)

plt.savefig('bla.png')