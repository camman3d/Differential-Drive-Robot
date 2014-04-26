import cv2
import math
import numpy as np

__author__ = 'josh'

# Variables
hue_range = 20
kernel_size = 20
thresh_cutoff = 127
hues = {
    "green": 40,
    "blue": 110,
    "red": -10,
    "pink": 160
}
sigma = 0.5


def threshold(img, hue_name):
    if hue_name.isdigit():
        hue = int(hue_name)
    else:
        hue = hues[hue_name]
    color_low = np.array([hue, 50, 50])
    color_high = np.array([hue + hue_range, 255, 255])

    # Threshold the HSV image to get only blue colors
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_low, color_high)

    # Convolve w/ a kernel and threshold again to remove noise
    mask2 = cv2.blur(mask, (kernel_size, kernel_size))
    _, mask2 = cv2.threshold(mask2, thresh_cutoff, 255, cv2.THRESH_BINARY)

    # Compute the "middle" for point tracking
    moments = cv2.moments(mask, True)
    area = moments["m00"]
    if area == 0:
        location = None
    else:
        location = int(moments["m10"] / area), int(moments["m01"] / area)

    res = cv2.bitwise_and(img, img, mask=mask)
    return area, location, res


def open_img(filename):
    return cv2.imread(filename)


def save_img(img, filename):
    return cv2.imwrite(filename, img)


def horizontal_weight(raw_weight, offset):
    if offset is None:
        return 0
    offset = offset * 2 - 1
    g_val = (2 / (sigma * math.sqrt(2 * math.pi))) * math.e ** (-(offset ** 2) / (2 * sigma ** 2))
    return raw_weight * g_val

obst_thresh = 1500
dest_thresh = 1500


def process(img, obst_hue, dest_hue, img_width):
    print("Obstacles: " + obst_hue + ", Destination: " + dest_hue)
    obst_result = threshold(img, obst_hue)
    dest_result = threshold(img, dest_hue)
    print(obst_hue + ": " + str(obst_result[0]))
    print(dest_hue + ": " + str(dest_result[0]))
    if obst_result[0] < obst_thresh:
        obst_result = 0, None
    if dest_result[0] < dest_thresh:
        dest_result = 0, None


    # Fuzzy value 1: obstacle horizontal offset
    if obst_result[1] is None:
        v1 = None
    else:
        v1 = float(obst_result[1][0]) / float(img_width)

    # Fuzzy value 2: destination horizontal offset
    if dest_result[1] is None:
        v2 = None
    else:
        v2 = float(dest_result[1][0]) / float(img_width)

    # Fuzzy value 3: balanced weight of obstacle to destination. 1 = all obst, 0 = all dest
    o_w = horizontal_weight(obst_result[0], v1)
    d_w = horizontal_weight(dest_result[0], v2)
    if o_w is 0 and d_w is 0:
        v3 = 0.5
    else:
        v3 = float(o_w) / float(d_w + o_w)

    return v1, v2, v3
