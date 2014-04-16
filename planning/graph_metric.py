import numpy as np
import matplotlib.pyplot as plt


__author__ = 'josh'


def plot_metric(world, last_dir, *metrics):
    x = np.arange(0, 2 * np.pi, 0.05)
    plots = ["b-", "g-", "r-", "c-", "m-"]
    for i in range(len(metrics)):
        metric = metrics[i]
        y = np.arange(0, 2 * np.pi, 0.05)
        for j in range(len(x)):
            y[j] = metric(x[j], world, last_dir)
        plt.plot(x, y, plots[i])
    plt.show()