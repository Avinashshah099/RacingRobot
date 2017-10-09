from __future__ import print_function, with_statement, division

import argparse

import cv2
import numpy as np

from image_processing import processImage

# Arrow keys
UP_KEY = 82
DOWN_KEY = 84
RIGHT_KEY = 83
LEFT_KEY = 81
ENTER_KEY = 10
SPACE_KEY = 32
EXIT_KEYS = [113, 27]  # Escape and q
S_KEY = 115  # Save key

play_video = False

parser = argparse.ArgumentParser(description='White Lane Detection for a batch of images')
parser.add_argument('-i', '--input_video', help='Input Video', default="debug/robot_vue.mp4", type=str)
parser.add_argument('-r', '--regions', help='ROI', default=1, type=int)
args = parser.parse_args()

# OpenCV 3.x.x compatibility
if not hasattr(cv2, 'cv'):
    # 0-based index of the frame to be decoded/captured next.
    image_zero_index = cv2.CAP_PROP_POS_FRAMES
    frame_count = cv2.CAP_PROP_FRAME_COUNT
else:
    image_zero_index = cv2.cv.CV_CAP_PROP_POS_FRAMES
    frame_count = cv2.cv.CV_CAP_PROP_FRAME_COUNT

video_file = args.input_video
cap = cv2.VideoCapture(video_file)

# Creating a window for later use
cv2.namedWindow('result')

def nothing(x):
    pass


current_idx = cap.get(image_zero_index)
n_frames = int(cap.get(frame_count))
print("{} frames".format(n_frames))
while True:
    while True:
        flag, img = cap.read()
        if flag:
            break
        else:
            # The next frame is not ready, so we try to read it again
            cap.set(image_zero_index, current_idx - 1)
            cv2.waitKey(1000)
            continue

    original_img = img.copy()
    resolution = (640 // 2, 480 // 2)
    max_width = resolution[0]
    # Regions of interest
    r0 = [0, 150, max_width, 50]
    r1 = [0, 125, max_width, 50]
    r2 = [0, 100, max_width, 50]
    r3 = [0, 75, max_width, 50]
    r4 = [0, 50, max_width, 50]
    regions = [r1, r2, r3]
    if args.regions == 0:
        regions = [[0, 0, img.shape[1], img.shape[0]]]
    processImage(img, debug=True, regions=regions)
    if not play_video:
        key = cv2.waitKey(0) & 0xff
    else:
        key = cv2.waitKey(10) & 0xff
    if key in EXIT_KEYS:
        cv2.destroyAllWindows()
        exit()
    elif key in [LEFT_KEY, RIGHT_KEY] or play_video:
        current_idx += 1 if key == RIGHT_KEY or play_video else -1
        current_idx = np.clip(current_idx, 0, n_frames - 1)
    elif key == SPACE_KEY:
        play_video = not play_video

    cap.set(image_zero_index, current_idx)
