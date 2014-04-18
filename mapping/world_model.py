import math
import numpy as np

__author__ = 'josh'


class WorldModel:

    def __init__(self, size=100, alpha=0):
        self.size = size
        self.alpha = alpha
        self.grid = np.zeros((2, size, size))

    def add_reading(self, angles, values):
        # Prepare for update
        self.grid[1] = np.zeros((self.size, self.size))

        # Sort the stuff
        data = zip(angles, values)
        data = sorted(data, key=lambda x: x[0])
        angles, values = map(lambda e: e[0], data), map(lambda e: e[1], data)

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
        # for x in range(self.size):
        #     for y in range(self.size):
        #         self.grid[0][x][y] = self.grid[1][x][y] + self.alpha * self.grid[0][x][y]
        self.grid[0] = self.grid[1]

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

    def get_reading(self, angle):
        reading_dist = 25
        x, y = self.size / 2 + reading_dist * math.cos(angle), self.size / 2 - reading_dist * math.sin(angle)
        return self.grid[0][x][y]

    def get_min(self):
        return np.min(self.grid[0])

    def get_max(self):
        return np.max(self.grid[0])

    def is_valid(self, angle):
        return True