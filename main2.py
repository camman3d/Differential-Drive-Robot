from fuzzy import controller
import image_processor
#from raspberrypi.robot_agent import RobotAgent
from simulation.vision_simulation_agent import VisionSimulationAgent

__author__ = 'josh'

# agent = VisionSimulationAgent([256, 256, 0], True, "env1.blend")
agent = VisionSimulationAgent([256, 256, 0], True, "env2.blend")
# agent = VisionSimulationAgent([256, 256, 0], True, "env3.blend")

# agent = RobotAgent()


turn_granularity = 0.2
move_distance = 5

while True:
    img = agent.get_image()
    fuzzy_vars = image_processor.process(img, agent.obst_hue, agent.dest_hue, agent.image_width)
    print("Fuzzy vars: " + str(fuzzy_vars))
    results = controller.processor(fuzzy_vars, controller.all_rules)
    print("Results: " + str(results))

    # Execute the action
    action = 0, -1
    for i in range(3):
        if results[i] > action[0]:
            action = results[0], i

    if action[1] is 0:
        print("Moving forward")
        agent.move_forward(move_distance)
    elif action[1] is 1:
        print("Turning left")
        agent.rotate_left(turn_granularity)
    elif action[1] is 2:
        print("Turning right")
        agent.rotate_right(turn_granularity)
