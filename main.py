from mapping import world_renderer
from mapping.world_model import WorldModel
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

agent = VisionSimulationAgent([256, 256, 0])
world = WorldModel(256)

while True:
    # Get readings
    angles, values = agent.get_full_readings()

    # Update the model of the world
    print("Updating world...")
    world.begin_update()
    world.add_reading((agent.robot[0] / 2, agent.robot[1] / 2), angles, values)
    world.end_update()

    # Render the world
    print("Rendering...")
    world_renderer.render(world)

    # Determine the next location
    # agent.robot[0] += 25
    agent.robot[1] = 50
