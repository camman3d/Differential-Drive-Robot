import math
import cv2

from blender_source import BlenderSource
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

blender = BlenderSource()


class VisionSimulationAgent:
    def __init__(self, robot):
        self.robot = robot
        self.last_img = None
        pass

    def get_image(self):
        blender.set(self.robot[0], self.robot[1], self.robot[2])
        img = blender.get()
        self.last_img = img
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
        attract = self.calculate_value(img, "red", destination_constant, profile)
        repel = self.calculate_value(img, "green", obstacle_constant, profile)
        return attract + repel

    def move_forward(self, duration):
        dx = math.cos(self.robot[2]) * robot_translation_speed * duration
        dy = math.sin(self.robot[2]) * robot_translation_speed * duration
        self.robot[0] += dx
        self.robot[1] += dy

    def move_backward(self, duration):
        dx = math.cos(self.robot[2]) * robot_translation_speed * duration
        dy = math.sin(self.robot[2]) * robot_translation_speed * duration
        self.robot[0] -= dx
        self.robot[1] -= dy

    def rotate_left(self, duration):
        self.robot[2] -= robot_rotation_speed * duration

    def rotate_right(self, duration):
        self.robot[2] += robot_rotation_speed * duration

        # agent = VisionSimulationAgent([256, 256, 0])
        #
        # ang = 0
        # foobar = ""
        # while ang < 2*math.pi:
        #     agent.robot[2] = ang
        #     # agent.robot[2] = 0.75*math.pi
        #     # img = agent.get_image()
        #
        #     # for i in range(0, 300):
        #     #     data = image_processor.threshold(img, "red")
        #     #     cv2.imshow('frame', data[2])
        #     #     print(i)
        #     #     k = cv2.waitKey(100) & 0xFF
        #
        #     # agent.move_backward(2)
        #     # agent.rotate_right(1)
        #
        #     # data = image_processor.threshold(img, "red")
        #
        #     # Normalize
        #     # value = min(20000, data[0])
        #     # weight = 1
        #     # offset = 0
        #     # if data[1] is not None:
        #     #     Offset contains a number from -1 to 1
        #         # offset = float(data[1][0] - 512) / 512.0
        #         # offset = 0
        #         # sigma = 0.5
        #         # weight = (2 / (sigma * math.sqrt(2 * math.pi))) * math.e ** (-(offset ** 2) / (2 * sigma ** 2))
        #     # value *= weight
        #
        #     value = agent.get_reading()
        #     foobar += str(ang) + "\t" + str(value) + "\n"
        #
        #     # font = cv2.FONT_HERSHEY_SIMPLEX
        #     # cv2.putText(img, str(offset), (10, 80), font, 1, (255, 255, 255), 2)
        #     # cv2.putText(img, str(weight), (10, 180), font, 1, (255, 255, 255), 2)
        #     # cv2.putText(img, str(value), (10, 180), font, 1, (255, 255, 255), 2)
        #
        #     cv2.imshow('frame1', agent.last_img)
        #     k = cv2.waitKey(5) & 0xFF
        #     # if k == 27:
        #     #     break
        #
        #     ang += 0.1
        # print(foobar)