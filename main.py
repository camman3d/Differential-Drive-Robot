import time
import math
from mapping import world_renderer
from mapping.world_model import WorldModel
from planning.direction_metric import max_metric, q_little_turn, q_reading, q_obstacle_edge, q_obstacle_buffer, q_main, \
    q_normalized_reading
from planning.graph_metric import plot_metric
from simulation.configuration import Configuration
from simulation.simulation_agent import SimulationAgent
# from simulation.vision_simulation_agent import VisionSimulationAgent
from simulation.vision_simulation_agent import VisionSimulationAgent

__author__ = 'josh'

agent = SimulationAgent(Configuration([255, 255, 0], (50, 250), [(150, 250), (150, 200), (150, 300)]))
# agent = SimulationAgent(Configuration([255, 255, 0], (100, 350), [(100, 250), (100, 200), (100, 300)]))
# agent = VisionSimulationAgent([256, 256, 0], True)
world = WorldModel()
last_dir = 0
turn_granularity = 0.2
show_stuff = True


def orient(angle):
    if agent.get_angle() > angle:
        da = agent.get_angle() - angle
        if da < math.pi:
            agent.rotate_right(da)
        else:
            agent.rotate_left(2*math.pi - da)
    else:
        da = angle - agent.get_angle()
        if da < math.pi:
            agent.rotate_left(da)
        else:
            agent.rotate_right(2*math.pi - da)


def update(u_angles, u_values):
    millis1 = int(round(time.time() * 1000))
    world.add_reading(u_angles, u_values)
    millis2 = int(round(time.time() * 1000))
    print("World model updated. (" + str(millis2 - millis1) + " ms)")


def get_reading(start, end):
    print("Getting reading from " + str(start) + " to " + str(end))
    agent.rotate_right(start)
    ang, angles, values = 0, [], []
    while ang < end - start:
        values.append(agent.get_reading())
        angles.append(agent.get_angle())
        ang += turn_granularity
        agent.rotate_left(turn_granularity)
    return angles, values


def get_full_readings():
    return get_reading(0, 2*math.pi)


def get_local_readings():
    return get_reading(math.pi/2, math.pi/2)


# First, get a full reading of the world
angles, values = get_full_readings()
update(angles, values)

# Figure out where we're going to go
best_dir = max_metric(world, last_dir, q_main)
print("Best direction: " + str(best_dir))

# Show stuff
if show_stuff:
    world_renderer.render(world, best_dir)
    # plot_metric(world, last_dir, q_normalized_reading)
    # plot_metric(world, last_dir, q_little_turn, q_obstacle_edge, q_normalized_reading, q_main)
    # plot_metric(world, last_dir, q_main)

# Now move
orient(best_dir)
agent.move_forward(3)
last_dir = best_dir

while True:
    # TODO: Get a local reading (180 deg ?)
    # angles, values = get_local_readings()
    angles, values = get_full_readings()
    update(angles, values)

    # Figure out where we're going to go
    best_dir = max_metric(world, last_dir, q_main)
    print("Best direction: " + str(best_dir))

    # Show stuff
    if show_stuff:
        world_renderer.render(world, best_dir)
        # plot_metric(world, last_dir, q_normalized_reading)
        # plot_metric(world, last_dir, q_little_turn, q_obstacle_edge, q_normalized_reading, q_main)

    # Now move
    best_dir = max_metric(world, last_dir, q_main)
    orient(best_dir)
    agent.move_forward(4)
    last_dir = best_dir