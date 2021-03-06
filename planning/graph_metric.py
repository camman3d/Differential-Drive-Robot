import numpy as np
import matplotlib.pyplot as plt


__author__ = 'josh'


def plot_metric(world, last_dir, *metrics):
    x = np.arange(0, 2 * np.pi, 0.05).tolist()
    x = np.array(filter(lambda a: world.is_valid(a), x))
    plots = ["b-", "g-", "r-", "c-", "m-"]
    for i in range(len(metrics)):
        metric = metrics[i]
        y = np.zeros(len(x))
        for j in range(len(x)):
            y[j] = metric(x[j], world, last_dir)
        plt.plot(x, y, plots[i])
    plt.show()