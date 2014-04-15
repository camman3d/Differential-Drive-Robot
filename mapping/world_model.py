import math
import numpy as np

__author__ = 'josh'


class WorldModel:

    def __init__(self, size=100, alpha=0):
        self.size = size
        self.alpha = alpha
        self.grid = np.zeros((2, size, size))

    def shift(self, d, theta):
        grid_2 = np.zeros((2, self.size, self.size))
        dx = d * math.cos(theta)
        dy = d * math.sin(theta)
        for x in range(self.size):
            for y in range(self.size):
                if 0 <= x + dx < self.size and 0 <= y + dy < self.size:
                    grid_2[0][x + dx][y + dy] = self.grid[0][x][y]
        self.grid = grid_2


    # def begin_update(self):
    #     self.grid
        # Push history
        # for x in range(self.size):
        #     for y in range(self.size):
        #         for i in range(1, self.history):
        #             self.grid[x][y][self.history - 1 - i] = self.grid[x][y][self.history - 2 - i]
        #         self.grid[x][y][0] = 0

    def add_reading(self, angles, values):
        # Prepare for update
        self.grid[1] = np.zeros((self.size, self.size))

        # Maximum interpolation step
        # angle_step = 0.025
        location = self.size / 2, self.size / 2

        def interpolate(ang0, ang1, val0, val1):
            if ang1 < ang0:
                ang1 += math.pi * 2

            # da, dv = ang1 - ang0, val1 - val0
            # while da > angle_step:
            #     da, dv = da / 2, dv / 2
            interpolation_granularity = float(self.size)
            da, dv = float(ang1 - ang0) / interpolation_granularity, float(val1 - val0) / interpolation_granularity

            while ang0 < ang1:
                self._draw_line(location, ang0, val0)
                ang0 += da
                val0 += dv

        for i in range(len(angles) - 1):
            interpolate(angles[i], angles[i+1], values[i], values[i+1])
        interpolate(angles[-1], angles[0], values[-1], values[0])

        # Work in last reading
        for x in range(self.size):
            for y in range(self.size):
                self.grid[0][x][y] = self.grid[1][x][y] + self.alpha * self.grid[0][x][y]

        # self._smooth()


    def _draw_line(self, location, angle, value):
        def plot(x, y):
            if 0 <= x < self.size and 0 <= y < self.size:
                self.grid[1][x][y] = value

        # Draw a line via Bresenham's line algorithm
        # http://en.wikipedia.org/wiki/Bresenham's_line_algorithm
        x0, y0 = int(location[0]), int(location[1])
        x1, y1 = int(x0 + math.cos(angle) * self.size), int(y0 + math.sin(angle) * self.size)

        dx = abs(x1-x0)
        dy = abs(y1-y0)
        if x0 < x1:
            sx = 1
        else:
            sx = -1
        if y0 < y1:
            sy = 1
        else:
            sy = -1
        err = dx - dy

        while True:
            plot(x0, y0)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2*err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    # def _average(self, x, y, margin=3):
    #     if x < margin:
    #         x = margin
    #     if y < margin:
    #         y = margin
    #     if x > self.size - margin - 1:
    #         x = self.size - margin - 1
    #     if y > self.size - margin - 1:
    #         y = self.size - margin - 1
    #
    #     value = self.grid[x][y][1]
    #     for i in range(margin):
    #         for j in range(margin):
    #             value += self.grid[x - margin + i][y - margin + i][1]
    #             value += self.grid[x - margin + i][y + margin - i][1]
    #             value += self.grid[x + margin - i][y - margin + i][1]
    #             value += self.grid[x + margin - i][y + margin - i][1]
    #     value /= (2*margin)**2
    #     return value
    #
    #
    # def _smooth(self):
    #     # TODO: Smooth by convolving w/ a Gaussian kernel
    #     kernel = [
    #         [0.00000067, 0.00002292, 0.00019117, 0.00038771, 0.00019117, 0.00002292, 0.00000067],
    #         [0.00002292, 0.00078634, 0.00655965, 0.01330373, 0.00655965, 0.00078633, 0.00002292],
    #         [0.00019117, 0.00655965, 0.05472157, 0.11098164, 0.05472157, 0.00655965, 0.00019117],
    #         [0.00038771, 0.01330373, 0.11098164, 0.22508352, 0.11098164, 0.01330373, 0.00038771],
    #         [0.00019117, 0.00655965, 0.05472157, 0.11098164, 0.05472157, 0.00655965, 0.00019117],
    #         [0.00002292, 0.00078633, 0.00655965, 0.01330373, 0.00655965, 0.00078633, 0.00002292],
    #         [0.00000067, 0.00002292, 0.00019117, 0.00038771, 0.00019117, 0.00002292, 0.00000067]
    #     ]
    #     # For each point
    #     grid_2 = np.zeros((self.size, self.size, 2))
    #     for x in range(3, self.size - 3):
    #         for y in range(3, self.size - 3):
    #             value = 0
    #             for i in range(7):
    #                 for j in range(7):
    #                     value = 2*kernel[i][j] * self.grid[x+i-3][y+j-3][0]
    #             grid_2[x][y][0] = value
    #     self.grid = grid_2



    # def end_update(self):
    #     # Incorporate history
    #     for x in range(self.size):
    #         for y in range(self.size):
    #             for i in range(1, self.history):
    #                 self.grid[x][y][0] += self.grid[x][y][i] / self._decay(i + 1)
