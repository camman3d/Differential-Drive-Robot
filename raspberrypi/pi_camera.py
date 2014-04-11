import os

__author__ = 'josh'


def read():
    # Perform pi camera read
    #os.system("/opt/vc/bin/raspicam -w 800 -h 600 -t 0 -o /tmp/capture.jpg")
    #os.system("/usr/bin/raspistill -w 800 -h 600 -o /tmp/capture.jpg -t 1")
    os.system("/usr/bin/raspistill -n -w 800 -h 600 -o /tmp/capture.jpg -awb auto -t 1 -ss 200000")
    return "/tmp/capture.jpg"
