def extract_blob(img_gray, img_rgb):
    blobs_log = blob_log(img_gray, max_sigma=30, num_sigma=10, threshold=.1)
    blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)    

    fig, ax = plt.subplots(1, 1)
    ax.set_title('Blob using Laplacian Of Gaussian', fontsize=18)
    ax.imshow(img_rgb, interpolation='nearest')
    ax.axis('off')

    min_r = 10 # in pixel
    for blob in blobs_log:
        y, x, r = blob
        if r >= min_r:
            c = plt.Circle((x, y), r, color='red', linewidth=2, fill=False)
            ax.add_patch(c)

    plt.tight_layout()
    plt.savefig('blob_log.png', interpolation='nearest')