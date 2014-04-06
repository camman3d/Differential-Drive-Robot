import sys
import image_processor
import pi_camera

__author__ = 'josh'

hue_num = sys.argv[1]

filename = pi_camera.read()
img = image_processor.open_img(filename)
area, location, res = image_processor.threshold(img, hue_num)

print("Results of image analysis for hue: " + hue_num)
print("  Area:   " + str(area))
print("  Center: " + str(location[0]) + ", " + str(location[1]))

image_processor.save_img(res, "/tmp/mask.jpg")