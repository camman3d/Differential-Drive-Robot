import math
import numpy as np

__author__ = 'josh'


class WorldModel:

    def __init__(self, size=100, history=3):
        self.size = size
        self.history = history
        self.grid = np.zeros((size, size, history))

    def _decay(self, i):
        # The bigger the decay, the less weight older readings have
        return i**2 / 2

    def begin_update(self):
        # Push history
        for x in range(self.size):
            for y in range(self.size):
                for i in range(1, self.history):
                    self.grid[x][y][self.history - 1 - i] = self.grid[x][y][self.history - 2 - i]
                self.grid[x][y][0] = 0

    def add_reading(self, location, angles, values):
        interpolation_granularity = self.size

        def interpolate(ang0, ang1, val0, val1):
            if ang1 < ang0:
                ang1 += math.pi * 2
            da, dv = (ang1 - ang0) / interpolation_granularity, (val1 - val0) / interpolation_granularity
            while ang0 < ang1:
                self.draw_line(location, ang0, val0)
                ang0 += da
                val0 += dv

        for i in range(len(angles) - 1):
            interpolate(angles[i], angles[i+1], values[i], values[i+1])
        interpolate(angles[-1], angles[0], values[-1], values[0])

    def draw_line(self, location, angle, value):
        def plot(x, y):
            if 0 <= x < self.size and 0 <= y < self.size:
                self.grid[x][y][0] = value

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

    def end_update(self):
        # Incorporate history
        for x in range(self.size):
            for y in range(self.size):
                for i in range(1, self.history):
                    self.grid[x][y][0] += self.grid[x][y][i] / self._decay(i + 1)
