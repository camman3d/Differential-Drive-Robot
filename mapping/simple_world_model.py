import math

__author__ = 'josh'


def in_range(first, second, angle):
    # First should be smaller than second
    if first <= second:
        return first <= angle <= second
    else:
        # We passed the origin (0 rad) so modify to take that into account
        da = 2 * math.pi - first
        second += da
        angle += da
        angle %= 2 * math.pi
        return 0 <= angle <= second


class SimpleWorldModel:
    def __init__(self):
        self.data = []

    def add_reading(self, angles, values):
        """This assumes the angles are going counter-clockwise (progressively bigger angles)"""
        self.data = zip(angles, values)

    def get_reading(self, angle):
        pass
        for i in range(len(self.data) - 1):
            if in_range(self.data[i][0], self.data[i + 1][0], angle):
                return self._interpolate_value(i, angle)
        return None

    def _interpolate_value(self, index, angle):
        a1, v1 = self.data[index]
        a2, v2 = self.data[index + 1]
        if a2 < a1:
            # We passed the origin (0 rad) so modify to take that into account
            da = 2 * math.pi - a1
            a1, a2, angle = 0, a2 + da, (angle + da) % 2 * math.pi
        percent = (angle - a1) / (a2 - a1)
        value = percent * v2 + (1 - percent) * v1
        return value

    def get_min(self):
        return min(map(lambda x: x[1], self.data))

    def get_max(self):
        return max(map(lambda x: x[1], self.data))

    def is_valid(self, angle):
        return in_range(self.data[0][0], self.data[-1][0], angle)


if __name__ == "__main__":
    print(in_range(1, 2, 1.5))  # T
    print(in_range(1, 2, 2.5))  # F
    print(in_range(5, 1, 0.5))  # T
    print(in_range(5, 1, 6))  # T
    print(in_range(5, 1, 1.5))  # F

    world = SimpleWorldModel()
    world.add_reading([0, 1, 2], [10, 20, 40])
    print(world.get_reading(0))  # 10
    print(world.get_reading(1))  # 20
    print(world.get_reading(2))  # 40

    print(world.get_reading(1.25))  # 25
    print(world.get_reading(1.5))  # 30
    print(world.get_reading(1.75))  # 35

    print(world.get_reading(0.25))  # 12.5
    print(world.get_reading(0.5))  # 15
    print(world.get_reading(0.75))  # 17.5

    world = SimpleWorldModel()
    world.add_reading([5, 6, 0, 1, 2], [1, 2, 3, 4, 5])
    print(world.is_valid(4.5))
    print(world.is_valid(5.5))
    print(world.is_valid(6.1))
    print(world.is_valid(0.1))
    print(world.is_valid(1.5))
    print(world.is_valid(2.5))