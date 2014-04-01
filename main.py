import math
from simulation_agent import SimulationAgent
from attract import attract_full
from configuration import Configuration
from vision_simulation_agent import VisionSimulationAgent

__author__ = 'josh'


# Find the best angle
print("Doing full search")
# agent = SimulationAgent(Configuration([255, 255, 0], (70, 80), [(300, 300), (330, 490), (280, 120)]))
agent = VisionSimulationAgent([256, 256, 0])
agent.search_full()

# Part B: Move forward, taking breaks to recalibrate
print("Moving...")
while True:
    agent.move_forward(1)
    agent.search_local()
