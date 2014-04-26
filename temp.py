import time

from raspberrypi import motors


__author__ = 'josh'

print("Testing left with t = 0.5")
raw_input()
motors.rotate_left()
time.sleep(0.5)
motors.stop()

print("Testing left with t = 1")
raw_input()
motors.rotate_left()
time.sleep(1)
motors.stop()

print("Testing left with t = 1.5")
raw_input()
motors.rotate_left()
time.sleep(1.5)
motors.stop()

print("Testing left with t = 2")
raw_input()
motors.rotate_left()
time.sleep(2)
motors.stop()

print("Testing left with t = 2.5")
raw_input()
motors.rotate_left()
time.sleep(2.5)
motors.stop()

print("Testing right with t = 0.5")
raw_input()
motors.rotate_right()
time.sleep(0.5)
motors.stop()

print("Testing right with t = 1")
raw_input()
motors.rotate_right()
time.sleep(1)
motors.stop()

print("Testing right with t = 1.5")
raw_input()
motors.rotate_right()
time.sleep(1.5)
motors.stop()

print("Testing right with t = 2")
raw_input()
motors.rotate_right()
time.sleep(2)
motors.stop()

print("Testing right with t = 2.5")
raw_input()
motors.rotate_right()
time.sleep(2.5)
motors.stop()

