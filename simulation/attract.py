import math

__author__ = 'josh'

destination_const = 1
obstacle_const = -1


def attract_normal(theta, sigma=math.pi / 10, cutoff=math.pi / 4):
    """Determine the base attractive force based on a Gaussian normal distribution"""
    # while theta < 0:
    #     theta += 2 * math.pi
    if abs(theta) > cutoff:
        return 0
    return (1 / (sigma * math.sqrt(2 * math.pi))) * math.e ** (-(theta ** 2) / (2 * sigma ** 2))


def attract(location, angle, target, attractive_constant):
    # Translate the coordinate system
    location = location[0], -location[1]
    target = target[0], -target[1]

    # Compute the angle between the robot and the target
    theta = math.atan2(target[1] - location[1], (target[0] - location[0])) % (math.pi * 2)

    delta_theta = theta - angle
    return attractive_constant * attract_normal(delta_theta)


def attract_full(config, angle):
    f = attract((config.robot[0], config.robot[1]), angle, config.destination, destination_const)
    for obstacle in config.obstacles:
        f += attract((config.robot[0], config.robot[1]), angle, obstacle, obstacle_const)
    return f


if __name__ == "__main__":
    ang = 1.570795
    while ang < math.pi:
        print(attract((50, 50), ang, (20, 20), 1))
        ang += 0.1