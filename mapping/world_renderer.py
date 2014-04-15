import cv2
import numpy as np
from mapping.world_model import WorldModel

__author__ = 'josh'
pixelSize = 2
showing = False


def render(world):
    global showing
    showing = False
    size = world.size * pixelSize
    img = np.zeros((size, size, 3))
    high = np.max(world.grid[0])
    low = np.min(world.grid[0])

    for x in range(world.size):
        for y in range(world.size):
            world_value = world.grid[0][x][y]
            value = 0
            if world_value > 0 and high > 1:
                value = (0, world_value / high, 0)
            elif world_value < 0 and low < 1:
                value = (0, 0, world_value / low)
            for x_p in range(pixelSize):
                for y_p in range(pixelSize):
                    img[pixelSize * y + y_p][pixelSize * x + x_p] = value

    cv2.imshow("World", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    testWorld = WorldModel()

    angles = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
    values = [0, -10, -30, 0, 30, 50, 3, 0, 0, -30, -20, -4, 0]
    testWorld.add_reading(angles, values)
    render(testWorld)

    testWorld.shift(20, 1)
    render(testWorld)

    angles = [0, 1, 2, 3, 4]
    values = [0, 20, 40, 20, 0]
    testWorld.add_reading(angles, values)
    render(testWorld)