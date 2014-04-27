from fuzzy import controller
import image_processor
# from raspberrypi.robot_agent import RobotAgent
from simulation.vision_simulation_agent import VisionSimulationAgent

__author__ = 'josh'

# agent = VisionSimulationAgent([256, 256, 0], True, "env1.blend")
#agent = VisionSimulationAgent([256, 256, 0], True, "env2.blend")
agent = VisionSimulationAgent([256, 256, 0], True, "env3.blend")

# agent = RobotAgent()

behaviors = {
    "-2": "Explore by moving",
    "-1": "Explore by turning",
    "0": "Explore by turning",
    "1": "Go forward to goal",
    "2": "Turn left to goal",
    "3": "Turn right to goal",
    "4": "Turn left to go around obj",
    "5": "Turn right to go around obj",
    "6": "Go forward around obj",
    "7": "Go forward around obj",
    "8": "Turn right back to obj",
    "9": "Turn left back to obj"
}

turn_granularity = 0.3
move_distance = 5
last_behavior = -1
last_turn = agent.rotate_left

while True:
    img = agent.get_image()
    fuzzy_vars = image_processor.process(img, agent.obst_hue, agent.dest_hue, agent.image_width)
    print("Fuzzy vars: " + str(fuzzy_vars))

    behavior = controller.get_behavior(fuzzy_vars, last_behavior)
    print("Behavior: " + behaviors[str(behavior)])
    last_behavior = behavior

    if behavior <= 0:
        last_turn(turn_granularity)
    if behavior <= -2:
        last_behavior = 0
        agent.move_forward(move_distance)
    elif behavior == 1 or behavior == 6 or behavior == 7:
        agent.move_forward(move_distance)
    elif behavior == 2 or behavior == 4 or behavior == 9:
        agent.rotate_left(turn_granularity)
        last_turn = agent.rotate_left
    elif behavior == 3 or behavior == 5 or behavior == 8:
        agent.rotate_right(turn_granularity)
        last_turn = agent.rotate_right


