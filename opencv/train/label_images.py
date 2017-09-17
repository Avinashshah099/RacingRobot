import os

import cv2
import numpy as np

from image_processing import processImage

EXIT_KEYS = [113, 27]  # Escape and q

input_folder = 'train/dataset/track4/'
output_folder = 'train/cropped/track4/'
images = [im for im in os.listdir(input_folder) if im.endswith('.jpg')]
print(len(images))

for idx, name in enumerate(images):
    img = cv2.imread('{}/{}'.format(input_folder, name))
    print(name)
    original_idx = name.split(".jpg")[0]
    original_img = img.copy()
    img = original_img.copy()
    max_width = img.shape[1]
    r0 = [0, 150, max_width, 50]
    r1 = [0, 125, max_width, 50]
    r2 = [0, 100, max_width, 50]
    regions = [r0, r1, r2]
    original_img = img.copy()
    for i, r in enumerate(regions):
        img = original_img.copy()
        margin_left, margin_top, _, _ = r
        im_cropped = original_img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        pts, turn_percent, centroids, errors = processImage(img, debug=True, regions=[r], interactive=True)
        if not all(errors):
            x, y = centroids.flatten()
            cx, cy = x - margin_left, y - margin_top
            cv2.imwrite('{}/{}-{}_{}-{}r{}.jpg'.format(output_folder, cx, cy, idx, original_idx, i), im_cropped)

    # key = cv2.waitKey(0) & 0xff
    # if key in EXIT_KEYS:
    #     break