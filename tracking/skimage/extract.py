from math import sqrt
from scipy import ndimage

import os
import glob

from skimage import io
from skimage import data, color
from skimage.color import rgb2gray

# from skimage.feature import blob_dog, blob_log, blob_doh
# from skimage.morphology import watershed
# from scipy import ndimage
# import matplotlib.pyplot as plt
# from skimage.feature import peak_local_max
# from skimage import data, img_as_float

from extract_hough import extract_hough_circle

def main():
    # input_img_dir = '/home/tor/jamu/xprmnt/cell/input/fps-10-sample'
    # output_img_dir = '/home/tor/jamu/xprmnt/cell/output-sample'
    input_img_dir = '/home/tor/jamu/xprmnt/cell/input/fps-10'
    output_img_dir = '/home/tor/jamu/xprmnt/cell/output'

    if not os.path.exists(output_img_dir):
        os.makedirs(output_img_dir)

    for filepath in glob.glob(os.path.join(input_img_dir, '*.png')):
        print('extracting: %s' % filepath)

        img_rgb = io.imread(filepath)
        img_gray = rgb2gray(img_rgb)
        out_filepath = output_img_dir+'/'+os.path.basename(filepath)

        extract_hough_circle(img_rgb, img_gray, out_filepath)

if __name__ == '__main__':
    main()
