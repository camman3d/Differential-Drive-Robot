import time
import motors

__author__ = 'josh'


motors.move_forward()
time.sleep(1)
motors.stop()
time.sleep(1)
motors.move_backward()
time.sleep(1)
motors.stop()
time.sleep(1)
motors.rotate_left()
time.sleep(1)
motors.stop()
time.sleep(1)
motors.rotate_right()
time.sleep(1)
motors.stop()
