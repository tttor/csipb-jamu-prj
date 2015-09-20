import numpy as np
import matplotlib.pyplot as plt

from skimage.transform import hough_circle
from skimage.transform import hough_ellipse
from skimage.draw import circle_perimeter
from skimage.draw import ellipse_perimeter
from skimage.util import img_as_ubyte
from skimage.feature import canny
from skimage.feature import peak_local_max

def extract_hough_circle(img_rgb, img_gray, out_filepath):
    # Canny
    img = img_as_ubyte(img_gray)
    edges = canny(img, sigma=3, low_threshold=10, high_threshold=50)

    # fig, ax = plt.subplots(nrows=1, ncols=1)
    # ax.imshow(edges, cmap=plt.cm.gray)
    # ax.axis('off')    
    # ax.set_title('Canny Edges for Hough Circle', fontsize=18)
    # plt.tight_layout()
    # plt.savefig('canny_edges_for_hough_circle.png')

    # Detect
    min_radii = 15; max_radii = 30; step_radii = 1
    plausible_radii = np.arange(min_radii, max_radii, step_radii)

    hough_circles = hough_circle(edges, plausible_radii)

    centers = []; accums = []; radii = []
    for radius, h in zip(plausible_radii, hough_circles):
        n_extracted_circle = 1 # ...for each radius
        peaks = peak_local_max(h, num_peaks=n_extracted_circle)
        centers.extend(peaks)
        accums.extend(h[peaks[:, 0], peaks[:, 1]])
        radii.extend([radius] * n_extracted_circle)

    # Draw the most prominent circles
    n_top_circle = 15
    fig, ax = plt.subplots(ncols=1, nrows=1)
    for idx in np.argsort(accums)[::-1][:n_top_circle]:
        center_x, center_y = centers[idx]
        center_color = (0, 225, 0)
        img_rgb[center_x, center_y] = center_color

        radius = radii[idx]
        perim_color = (255, 0, 0)
        perim_x_list, perim_y_list = circle_perimeter(center_y, center_x, radius)
        # if all(i < img_rgb.shape[1] for i in perim_x_list) and all(i < img_rgb.shape[0] for i in perim_y_list):
        #     img_rgb[perim_y_list, perim_x_list] = perim_color
        for perim_x, perim_y in zip(perim_x_list, perim_y_list):
            if perim_x < img_rgb.shape[1] and perim_y < img_rgb.shape[0]:
                img_rgb[perim_y, perim_x] = perim_color

    ax.imshow(img_rgb, cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('Hough Circle', fontsize=18)
    plt.tight_layout()
    plt.savefig(out_filepath)
    plt.close(fig)
