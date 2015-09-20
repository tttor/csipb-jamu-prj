'''
Extract circular-like (cell) objects

Options:
> hough tranform
> blob
> watershed
'''
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from scipy import ndimage

from skimage import io
from skimage import data, color
from skimage.color import rgb2gray
from skimage.feature import peak_local_max, canny
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.transform import hough_circle
from skimage.util import img_as_ubyte
from skimage.draw import circle_perimeter
from skimage.morphology import watershed
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
from scipy import ndimage
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
from skimage import data, img_as_float
from scipy import ndimage as ndi

def extract_canny(image):
    edges = canny(image, sigma=4)

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.imshow(edges, cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('Canny filter, $\sigma=1$', fontsize=20)
    plt.show()

def extract_watershed(image):
    # Now we want to separate the two objects in image
    # Generate the markers as local maxima of the distance
    # to the background    
    distance = ndi.distance_transform_edt(image)
    local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)),
                                labels=image)
    markers = ndi.label(local_maxi)[0]
    labels = watershed(-distance, markers, mask=image)
    print len(labels)

    fig, axes = plt.subplots(ncols=3, figsize=(8, 2.7))
    ax0, ax1, ax2 = axes

    ax0.imshow(image, cmap=plt.cm.gray, interpolation='nearest')
    ax0.set_title('Overlapping objects')
    ax1.imshow(-distance, cmap=plt.cm.jet, interpolation='nearest')
    ax1.set_title('Distances')
    ax2.imshow(labels, cmap=plt.cm.spectral, interpolation='nearest')
    ax2.set_title('Separated objects')

    for ax in axes:
        ax.axis('off')

    fig.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0,
                        right=1)
    plt.show()

def extract_blob(image_gray):
    blobs_log = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=.1)
    # Compute radii in the 3rd column.
    blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

    blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.1)
    blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

    blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.01)

    blobs_list = [blobs_log, blobs_dog, blobs_doh]
    colors = ['yellow', 'lime', 'red']
    titles = ['LaplacianOfGaussian', 'DifferenceOfGaussian',
              'DeterminantOfHessian']
    sequence = zip(blobs_list, colors, titles)

    for blobs, color, title in sequence:
        fig, ax = plt.subplots(1, 1)
        ax.set_title(title)
        # ax.imshow(image_gray, interpolation='nearest')
        ax.imshow(image_gray)
        for blob in blobs:
            y, x, r = blob
            c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
            ax.add_patch(c)

        plt.savefig('blob.'+title+'.png', interpolation='nearest')

def extract_hough(img_gray):
    img = img_as_ubyte(img_gray)
    edges = canny(img, sigma=5, low_threshold=10, high_threshold=50)

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.imshow(edges, cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('Canny filter', fontsize=20)
    plt.savefig('canny_edges.png')

    # Detect two radii
    hough_radii = np.arange(15, 30, 2)
    hough_res = hough_circle(edges, hough_radii)
    print len(hough_res)

    centers = []
    accums = []
    radii = []

    for radius, h in zip(hough_radii, hough_res):
        # For each radius, extract two circles
        num_peaks = 2
        peaks = peak_local_max(h, num_peaks=num_peaks)
        centers.extend(peaks)
        accums.extend(h[peaks[:, 0], peaks[:, 1]])
        radii.extend([radius] * num_peaks)

    # Draw the most prominent 15 circles
    fig, ax = plt.subplots(ncols=1, nrows=1)
    img_rgb = color.gray2rgb(img)
    for idx in np.argsort(accums)[::-1][:15]:
        center_x, center_y = centers[idx]
        radius = radii[idx]
        cx, cy = circle_perimeter(center_y, center_x, radius)
        img_rgb[cy, cx] = (220, 20, 20)

    ax.imshow(img_rgb, cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('Hough Circle', fontsize=20)
    plt.tight_layout()
    plt.savefig('hough.png')

def extract_hough_ellipse(image_gray):
    edges = canny(image_gray, sigma=3.0, low_threshold=0.55, high_threshold=0.8)

    # Perform a Hough Transform
    # The accuracy corresponds to the bin size of a major axis.
    # The value is chosen in order to get a single high accumulator.
    # The threshold eliminates low accumulators
    print 'hough_ellipse'
    result = hough_ellipse(edges, accuracy=20, threshold=250,
                           min_size=100, max_size=120)
    result.sort(order='accumulator')
    print len(result)

    # Estimated parameters for the ellipse
    best = result[-1]
    yc = int(best[1])
    xc = int(best[2])
    a = int(best[3])
    b = int(best[4])
    orientation = best[5]

    # # Draw the ellipse on the original image
    # cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
    # image_rgb[cy, cx] = (0, 0, 255)
    # # Draw the edge (white) and the resulting ellipse (red)
    # edges = color.gray2rgb(edges)
    # edges[cy, cx] = (250, 0, 0)

    # fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4))

    # ax1.set_title('Original picture')
    # ax1.imshow(image_rgb)

    # ax2.set_title('Edge (white) and result (red)')
    # ax2.imshow(edges)

    # plt.show()

def extract_local_max(img_gray):
    im = img_as_float(img_gray)

    # image_max is the dilation of im with a 20*20 structuring element
    # It is used within peak_local_max function
    image_max = ndimage.maximum_filter(im, size=20, mode='constant')

    # Comparison between image_max and im to find the coordinates of local maxima
    coordinates = peak_local_max(im, min_distance=20)

    # display results
    fig, ax = plt.subplots(1, 3, figsize=(8, 3))
    ax1, ax2, ax3 = ax.ravel()
    ax1.imshow(im, cmap=plt.cm.gray)
    ax1.axis('off')
    ax1.set_title('Original')

    ax2.imshow(image_max, cmap=plt.cm.gray)
    ax2.axis('off')
    ax2.set_title('Maximum filter')

    ax3.imshow(im, cmap=plt.cm.gray)
    ax3.autoscale(False)
    ax3.plot(coordinates[:, 1], coordinates[:, 0], 'r.')
    ax3.axis('off')
    ax3.set_title('Peak local max')

    fig.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
                        bottom=0.02, left=0.02, right=0.98)

    plt.show()

def main():
    # img_gray = data.coins()
    img_rgb = io.imread('cell.png')
    img_gray = rgb2gray(img_rgb)

    # extract_hough(img_gray)
    # extract_hough_ellipse(img_gray)
    # extract_blob(img_gray)
    extract_watershed(img_gray)
    # extract_canny(img_gray)
    # extract_local_max(img_gray)

if __name__ == '__main__':
    main()