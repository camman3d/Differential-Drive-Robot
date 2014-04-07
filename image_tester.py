import sys
import image_processor
import cv2

__author__ = 'josh'

in_filename = sys.argv[1]
hue_num = sys.argv[2]

img = image_processor.open_img(in_filename)

if hue_num == "all":
    for i in range(300):
        area, location, res = image_processor.threshold(img, str(i))
        print("Results of image analysis for hue: " + str(i))
        print("  Area:   " + str(area))
        if location is None:
            print("  Center: None")
        else:
            print("  Center: " + str(location[0]) + ", " + str(location[1]))
        cv2.imshow("image", res)
        cv2.waitKey(5)

else:
    area, location, res = image_processor.threshold(img, hue_num)
    print("Results of image analysis for hue: " + hue_num)
    print("  Area:   " + str(area))
    if location is None:
        print("  Center: None")
    else:
        print("  Center: " + str(location[0]) + ", " + str(location[1]))
    out_filename = sys.argv[3]
    image_processor.save_img(res, out_filename)