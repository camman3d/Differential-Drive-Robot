from vision_simulation_agent import VisionSimulationAgent

__author__ = 'josh'

agent = VisionSimulationAgent([256, 256, 0])

while True:
    agent.rotate_left(1)
    reading = agent.get_reading(True)
    print(reading)