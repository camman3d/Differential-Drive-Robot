import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from attract import attract_full
from configuration import Configuration

__author__ = 'josh'


def plot_configuration_attraction(config):
    x = np.arange(0, 2*np.pi, 0.05)
    y = np.vectorize(lambda ang: attract_full(config, ang))(x)
    plt.plot(x, y, "b-", [config.robot[2], config.robot[2]], [np.min(y), np.max(y)], "r-")
    # plt.plot()
    plt.show()


def draw_configuration(config):
    img = np.zeros((512, 512, 3), np.uint8)
    size = 20

    # Draw the robot w/ a circle and a line
    cv2.circle(img, (int(config.robot[0]), int(config.robot[1])), size, (255, 0, 0), 3)
    pt2 = int(config.robot[0] + size * math.cos(config.robot[2])), int(config.robot[1] + size * math.sin(config.robot[2]))
    cv2.line(img, (int(config.robot[0]), int(config.robot[1])), pt2, (255, 0, 0), 2)

    # Draw the destination
    cv2.circle(img, (int(config.destination[0]), int(config.destination[1])), size, (0, 255, 0), 3)

    # Draw the obstacles
    for obstacle in config.obstacles:
        cv2.circle(img, (int(obstacle[0]), int(obstacle[1])), size, (0, 0, 255), 3)

    cv2.imshow('frame', img)


# c = Configuration([255, 255, 0], (70, 80), [(300, 300), (330, 490), (280, 120)])
# plot_configuration_attraction(c)
# draw_configuration(c)
# input("")