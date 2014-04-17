import math
import time

import image_processor
import pi_camera
from raspberrypi import motors


__author__ = 'josh'

rotation_granularity = 0.5
reading_threshold = 0

robot_translation_time = 3
robot_rotation_time = 1

cap = 20000
sigma = 0.5
image_width = 800
destination_constant = 1
obstacle_constant = -1

left_speed = 0.745643442
right_speed = 0.688740167



class RobotAgent:
    def __init__(self):
        self.last_img = None
        self.angle = 0
        pass

    def get_image(self):
        return pi_camera.read()

    def search_full(self):
        """This will rotate the robot until the best angle is discovered"""

        print("Determining best path....")

        reading = self.get_reading()
        last = -9999.9
        while reading >= last or reading <= reading_threshold:
            last = reading
            self.rotate_left(rotation_granularity)
            reading = self.get_reading()
        self.rotate_right(rotation_granularity)

    def search_local(self):
        """This will recalibrate the robot to turn to the optimal direction"""

        print("Adjusting path...")

        reading = self.get_reading()
        last = -9999.9
        while reading >= last:
            last = reading
            self.rotate_left(rotation_granularity)
            reading = self.get_reading()
        last = -9999.9
        while reading >= last:
            last = reading
            self.rotate_right(rotation_granularity)
            reading = self.get_reading()
        self.rotate_left(rotation_granularity)

    @staticmethod
    def calculate_value(img, color, constant, profile=False):
        # Do image analysis
        data = image_processor.threshold(img, color)

        # Normalize
        if profile:
            value = data[0]
        else:
            value = min(cap, data[0])
        if data[1] is not None:
            # Offset contains a number from -1 to 1
            w = image_width / 2
            offset = float(data[1][0] - w) / w
            weight = (2 / (sigma * math.sqrt(2 * math.pi))) * math.e ** (-(offset ** 2) / (2 * sigma ** 2))
            value *= weight
        return value * constant

    def get_reading(self):
        img = image_processor.open_img(self.get_image())
        attract = self.calculate_value(img, "green", destination_constant)
        repel = self.calculate_value(img, "pink", obstacle_constant)
        return attract + repel

    def move_forward(self, duration):
        motors.move_forward()
        time.sleep(duration * robot_translation_time)
        motors.stop()

    def move_backward(self, duration):
        motors.move_backward()
        time.sleep(duration * robot_translation_time)
        motors.stop()

    def rotate_left(self, theta):
        duration = left_speed * theta
        motors.rotate_left()
        time.sleep(duration)
        motors.stop()
        self.angle += theta
        self.angle %= 2*math.pi

    def rotate_right(self, theta):
        duration = right_speed * theta
        motors.rotate_right()
        time.sleep(duration)
        motors.stop()
        self.angle -= theta
        self.angle %= 2*math.pi

    def get_angle(self):
        return self.angle