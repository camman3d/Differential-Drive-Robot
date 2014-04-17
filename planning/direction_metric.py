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
    x, y = world.size / 2 + reading_dist * math.cos(theta), world.size / 2 - reading_dist * math.sin(theta)
    return world.grid[0][x][y]


def q_little_turn(theta, w, last_theta):
    """Rewards for not turning very much"""
    d_theta = abs(theta - last_theta)
    return abs(math.pi - d_theta) / math.pi


def q_enumerated_policy(reading, policy):
    for i in range(len(policy) - 1):
        low = policy[i][0]
        high = policy[i + 1][0]
        if low <= reading <= high:
            percent = (reading - low) / (high - low)
            val = percent * policy[i][1] + (1 - percent) * policy[i+1][1]
            return val
    return 0


def q_obstacle_edge(theta, world, lt):
    """Rewards for heading to an obstacle edge"""
    # This policy is ok, but it brings the robot too close to the obstacles
    # policy = [
    #     (0, 0),
    #     (0.05, 0),
    #     (0.15, 0.75),
    #     (0.2, 1),
    #     (0.25, 0.75),
    #     (0.3, 0.25),
    #     (0.4, 0)
    # ]
    policy = [
        (0, 0),
        (0.03, 0),
        (0.1, 1),
        (0.15, 0),
        # (0.2, 1),
        # (0.25, 0.75),
        # (0.3, 0.25),
        # (0.4, 0)
    ]
    w_max = abs(np.min(world.grid[0]))
    reading = abs(q_reading(theta, world, 0)) / w_max
    val = q_enumerated_policy(reading, policy)
    return val


def q_obstacle_buffer(theta, world, lt):
    """Rewards for keeping distance from obstacles"""
    def f(x):
        return q_reading(x, world, lt)
    slope = derivative(f, theta)
    return max(min(1 - abs(slope), 1), 0)


def q_normalized_reading(theta, world, lt):
    w_max = np.max(world.grid[0])
    w_min = np.min(world.grid[0])
    reading = q_reading(theta, world, lt)
    if reading < 0:
        return 0.5 - abs(reading / w_min) / 2
    else:
        if w_max == 0:
            return 0.5
        return 0.5 + abs(reading / w_max) / 2


def q_combined(theta, world, last_theta, metrics, weights):
    val = 1
    for i in range(len(metrics)):
        result = metrics[i](theta, world, last_theta) * weights[i]
        result += 1 - weights[i]
        val *= result
    return val


def q_explore(theta, world, last_theta):
    # metrics = [q_obstacle_edge, q_little_turn, q_obstacle_buffer]
    # weights = [1, 0.5, 0.3]
    metrics = [q_obstacle_edge, q_little_turn, q_normalized_reading]
    weights = [0.8, 0.5, 1]
    return q_combined(theta, world, last_theta, metrics, weights)


def q_destination(theta, world, last_theta):
    metrics = [q_obstacle_edge, q_little_turn, q_normalized_reading]
    weights = [0.7, 0.3, 1]
    return q_combined(theta, world, last_theta, metrics, weights)


def q_main(theta, world, last_theta, threshold=0.75):
    reading = q_normalized_reading(theta, world, last_theta)
    if reading > threshold:
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