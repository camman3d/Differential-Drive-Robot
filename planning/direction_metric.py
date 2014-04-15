import math
import numpy as np

__author__ = 'josh'


reading_dist = 25


def derivative(f, x, dx=0.1):
    # Estimate the derivative based on seven readings.
    # Using seven readings provides a decent amount of smoothing
    reading0 = f(x - 3*dx)
    reading1 = f(x - 2*dx)
    reading2 = f(x - dx)
    reading3 = f(x)
    reading4 = f(x + dx)
    reading5 = f(x + 2*dx)
    reading6 = f(x + 3*dx)

    e_0 = (reading0 - reading3) / (-3 * dx)
    e_1 = (reading1 - reading3) / (-2 * dx)
    e_2 = (reading2 - reading3) / (-dx)
    e_4 = (reading4 - reading3) / dx
    e_5 = (reading5 - reading3) / (2 * dx)
    e_6 = (reading6 - reading3) / (3 * dx)
    return (e_0 + e_1 + e_2 + e_4 + e_5 + e_6) / 6


def q_reading(theta, world, lt):
    x, y = world.size / 2 + reading_dist * math.cos(theta), world.size / 2 + reading_dist * math.sin(theta)
    return world.grid[0][x][y]


def q_little_turn(theta, w, last_theta):
    """Rewards for not turning very much"""
    d_theta = abs(theta - last_theta)
    return abs(math.pi - d_theta) / math.pi + 1


def q_obstacle_edge(theta, world, lt):
    """Rewards for heading to an obstacle edge"""
    w_max = abs(np.min(world.grid[0]))
    policy = [
        (0.01, 0.1, 1),
        (0.1, 0.2, 2),
        (0.2, 0.3, 1),
        (0.3, 0.35, 0.4),
        (0.35, 0.65, 0.1),
        (0.55, 0.65, -0.1),
        (0.65, 0.9, -0.9),
        (0.9, 1, -1)
    ]
    reading = abs(q_reading(theta, world, lt))
    for p in policy:
        low = p[0] * w_max
        high = p[1] * w_max
        if low <= reading <= high:
            return p[2]
    return 0


def q_obstacle_buffer(theta, world, lt):
    """Rewards for keeping distance from obstacles"""
    def f(x):
        return q_reading(x, world, lt)
    slope = derivative(f, theta)
    return 1 - min(abs(slope), 1)


def q_explore(theta, world, last_theta):
    a = q_obstacle_edge(theta, world, last_theta)
    b = q_little_turn(theta, world, last_theta)
    c = 0.5 * q_obstacle_buffer(theta, world, last_theta) + 0.1
    return a * b * c


def q_destination(theta, world, last_theta):
    a = q_reading(theta, world, last_theta)
    b = q_obstacle_buffer(theta, world, last_theta)
    return a * b


def q_main(theta, world, last_theta):
    w_max = np.max(world.grid[0])
    if w_max > 0:
        return q_destination(theta, world, last_theta)
    else:
        return q_explore(theta, world, last_theta)



def max_metric(world, last_theta, metric):
    x = np.arange(0, 2 * np.pi, 0.05)
    y = np.vectorize(lambda ang: metric(ang, world, last_theta))(x)

    m_max = (0, 0)
    for i in range(len(x)):
        if y[i] > m_max[1]:
            m_max = x[i], y[i]
    return m_max[0]