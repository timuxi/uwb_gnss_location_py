import numpy as np
from matplotlib import pyplot as plt


class PltUtil:
    theta = np.arange(0, 2 * np.pi, 0.01)

    @staticmethod
    def pltCircle(a, b, r, color='y'):
        x = a + r * np.cos(PltUtil.theta)
        y = b + r * np.sin(PltUtil.theta)
        plt.plot(a, b, 'o', alpha=0.1, color='k')
        plt.plot(x, y, alpha=0.1, color=color)
