import cv2
import numpy as np

__author__ = 'josh'

# Variables
hue_range = 20
kernel_size = 20
thresh_cutoff = 127
hues = {
    "green": 40,
    "blue": 110,
    "red": -10
}


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