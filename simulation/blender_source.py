from subprocess import check_call
import cv2

__author__ = 'josh'


class BlenderSource:

    def __init__(self):
        env_path = "/Users/josh/Documents/School/Spring 2014/Robotics/Blender Environments/"
        self.image_dest = "render"
        self.camera = env_path + "camera.data"
        self.image_file = env_path + self.image_dest + "0000.png"
        self.blender = "/Applications/Blender/blender.app/Contents/MacOS/blender"
        self.env = env_path + "env1.blend"
        self.script = env_path + "position.py"

    def get(self):
        # Run the blender script
        # blender -b env1.blend -P position.py -x 1 -o //render -f 0
        check_call([self.blender, "-b", self.env, "-P", self.script, "-x", "1", "-o", "//" + self.image_dest, "-f", "0"])
        return cv2.imread(self.image_file)

    def set(self, x, y, rot):
        with open(self.camera, "w") as f:
                f.write(str(x) + "\n")
                f.write(str(y) + "\n")
                f.write(str(rot))
                f.close()