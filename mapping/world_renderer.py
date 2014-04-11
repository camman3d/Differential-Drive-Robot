import cv2
import numpy as np

__author__ = 'josh'
pixelSize = 2


def render(world):
    size = len(world.grid) * pixelSize
    img = np.zeros((size, size, 3))
    high = np.max(world.grid)
    low = np.min(world.grid)

    for x in range(len(world.grid)):
        for y in range(len(world.grid)):
            world_value = world.grid[x][y][0]
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

