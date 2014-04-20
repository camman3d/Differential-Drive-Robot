import cv2
import math
from simulation.vision_simulation_agent import VisionSimulationAgent

__author__ = 'josh'


agent = VisionSimulationAgent([256, 156, 3 * math.pi / 4], True)
agent.show(True)
cv2.waitKey(0)