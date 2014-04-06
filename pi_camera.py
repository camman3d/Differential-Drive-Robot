import os

__author__ = 'josh'


def read():
    # Perform pi camera read
    os.system("/opt/vc/bin/raspicam -w 800 -h 600 -t 0 -o /tmp/capture.jpg")
    return "/tmp/capture.jpg"