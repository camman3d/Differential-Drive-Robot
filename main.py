import time
from mapping import world_renderer
from mapping.world_model import WorldModel
from planning.direction_metric import max_metric, q_little_turn, q_reading, q_obstacle_edge, q_obstacle_buffer, q_main
from planning.graph_metric import plot_metric
from simulation.configuration import Configuration
from simulation.simulation_agent import SimulationAgent
from simulation.vision_simulation_agent import VisionSimulationAgent

__author__ = 'josh'


# # Find the best angle
# print("Doing full search")
# # agent = SimulationAgent(Configuration([255, 255, 0], (70, 80), [(300, 300), (330, 490), (280, 120)]))
# agent = VisionSimulationAgent([256, 256, 0])
# agent.search_full()
#
# # Part B: Move forward, taking breaks to recalibrate
# print("Moving...")
# while True:
#     agent.move_forward(1)
#     agent.search_local()


agent = SimulationAgent(Configuration([255, 255, 0], (50, 250), [(100, 250), (100, 200), (100, 300)]))
# agent = VisionSimulationAgent([256, 256, 0], True)
world = WorldModel()
last_dir = 0

while True:
    # Get readings
    angles, values = agent.get_full_readings()

    # Update the model of the world
    print("Updating world...")
    millis1 = int(round(time.time() * 1000))
    world.add_reading(angles, values)
    millis2 = int(round(time.time() * 1000))
    print("Done. Time taken: " + str(millis2 - millis1) + " ms")

    # Render the world
    # print("Rendering...")
    # world_renderer.render(world)

    # print("Graphing metric...")
    # print("Optimal direction: " + str(best_dir))


    # plot_metric(world, last_dir, q_reading)
    # plot_metric(world, last_dir, q_little_turn)

    # plot_metric(world, last_dir, q_obstacle_edge)
    # plot_metric(world, last_dir, q_obstacle_buffer)

    # def my_metric(theta, world, last_theta):
    #     a = q_reading(theta, world, last_theta)
    #     b = q_obstacle_buffer(theta, world, last_theta)
    #     return a * b
    #
    # plot_metric(world, last_dir, my_metric)
    best_dir = max_metric(world, last_dir, q_main)

    agent.orient(best_dir)
    agent.move_forward(3)
    last_dir = best_dir
