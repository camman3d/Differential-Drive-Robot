import numpy as np
import matplotlib.pyplot as plt


__author__ = 'josh'


def plot_metric(world, last_dir, metric):
    x = np.arange(0, 2 * np.pi, 0.05)
    y = np.vectorize(lambda ang: metric(ang, world, last_dir))(x)
    plt.plot(x, y, "b-")
    plt.show()