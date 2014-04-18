import math

import cv2

from simulation.blender_source import BlenderSource
import image_processor


__author__ = 'josh'

rotation_granularity = 0.25
reading_threshold = 0
robot_translation_speed = 10
robot_rotation_speed = 0.4

cap = 20000
sigma = 0.5
image_width = 1024
destination_constant = 1
obstacle_constant = -1


class VisionSimulationAgent:
    def __init__(self, robot, show_img, env):
        self.robot = robot
        self.last_img = None
        self.show_img = show_img
        self.blender = BlenderSource(env)
        pass

    def get_image(self):
        self.blender.set(self.robot[0], self.robot[1], self.robot[2])
        img = self.blender.get()
        self.last_img = img

        if self.show_img:
            self.show()

        return img

    def show(self, render=False):
        if render:
            self.get_image()
        cv2.imshow('frame', self.last_img)
        cv2.waitKey(5)

    def search_full(self):
        """This will rotate the robot until the best angle is discovered"""

        print("Determining best path....")

        reading = self.get_reading()
        last = -9999.9
        while reading >= last or reading <= reading_threshold:
            last = reading
            self.rotate_left(rotation_granularity)
            reading = self.get_reading()

            self.show()
        self.rotate_right(rotation_granularity)
        self.show(True)

        # graph.plot_configuration_attraction(self.config)

    def search_local(self):
        """This will recalibrate the robot to turn to the optimal direction"""

        print("Adjusting path...")

        reading = self.get_reading()
        last = -9999.9
        while reading >= last:
            last = reading
            self.rotate_left(rotation_granularity)
            reading = self.get_reading()
            self.show()
        last = -9999.9
        while reading >= last:
            last = reading
            self.rotate_right(rotation_granularity)
            reading = self.get_reading()
            self.show()
        self.rotate_left(rotation_granularity)
        self.show(True)


        # graph.plot_configuration_attraction(self.config)

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

    def get_reading(self, profile=False):
        img = self.get_image()
        attract = self.calculate_value(img, "green", destination_constant, profile)
        repel = self.calculate_value(img, "red", obstacle_constant, profile)
        return attract + repel

    def move_forward(self, duration):
        dx = math.cos(self.robot[2]) * robot_translation_speed * duration
        dy = math.sin(self.robot[2]) * robot_translation_speed * duration
        self.robot[0] += dx
        self.robot[1] += dy

        if self.show_img:
            self.show(True)

    def move_backward(self, duration):
        dx = math.cos(self.robot[2]) * robot_translation_speed * duration
        dy = math.sin(self.robot[2]) * robot_translation_speed * duration
        self.robot[0] -= dx
        self.robot[1] -= dy

    def rotate_left(self, theta):
        self.robot[2] += theta
        self.robot[2] %= math.pi * 2

    def rotate_right(self, theta):
        self.robot[2] -= theta
        self.robot[2] %= math.pi * 2

    def get_angle(self):
        return self.robot[2]