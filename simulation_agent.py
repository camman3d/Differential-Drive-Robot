import math
import cv2
from attract import attract_full
import graph


__author__ = 'josh'

time_step = 0.05
rotation_granularity = 0.25
reading_threshold = 0
robot_translation_speed = 1
robot_rotation_speed = 0.05


class SimulationAgent:
    def __init__(self, config):
        self.config = config
        pass

    def search_full(self):
        """This will rotate the robot until the best angle is discovered"""

        reading = self.get_reading()
        last = -9999.9
        while reading >= last or reading <= reading_threshold:
            last = reading
            self.rotate_left(rotation_granularity)
            reading = self.get_reading()
        self.rotate_right(rotation_granularity)

        # graph.plot_configuration_attraction(self.config)

    def search_local(self):
        """This will recalibrate the robot to turn to the optimal direction"""

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

        # graph.plot_configuration_attraction(self.config)

    def get_reading(self):
        return attract_full(self.config, self.config.robot[2])

    def move_forward(self, duration):
        t = 0
        while t < duration:
            dx = math.cos(self.config.robot[2]) * robot_translation_speed
            dy = math.sin(self.config.robot[2]) * robot_translation_speed
            self.config.robot[0] += dx
            self.config.robot[1] += dy

            # Draw and wait
            graph.draw_configuration(self.config)
            t += time_step
            cv2.waitKey(int(time_step * 100))

            # graph.plot_configuration_attraction(self.config)

    def move_backward(self, duration):
        t = 0
        while t < duration:
            dx = math.cos(self.config.robot[2]) * robot_translation_speed
            dy = math.sin(self.config.robot[2]) * robot_translation_speed
            self.config.robot[0] -= dx
            self.config.robot[1] -= dy

            # Draw and wait
            graph.draw_configuration(self.config)
            t += time_step
            cv2.waitKey(int(time_step * 100))

    def rotate_left(self, duration):
        t = 0
        while t < duration:
            self.config.robot[2] += robot_rotation_speed

            # Draw and wait
            graph.draw_configuration(self.config)
            t += time_step
            cv2.waitKey(int(time_step * 100))

    def rotate_right(self, duration):
        t = 0
        while t < duration:
            self.config.robot[2] -= robot_rotation_speed

            # Draw and wait
            graph.draw_configuration(self.config)
            t += time_step
            cv2.waitKey(int(time_step * 100))