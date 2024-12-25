from magnetic_tweezer.cpu_tracker import BeadCPUTracker
from magnetic_tweezer.cpu_tracker import bilinear_interpolate
from scipy.interpolate import RegularGridInterpolator
import numpy as np


BeadCPUTracker()


def test_bilinear_interpolate():
    # def f(x, y):
    #     return x ** 2 + y ** 2

    xlim, ylim = np.array([0, 1]), np.array([0, 1])

    # xv, yv = np.meshgrid(xlim, ylim, indexing='ij')
    # data = f(xv, yv)

    data = np.array(((0, 4), (1, 5)))
    interp = RegularGridInterpolator((xlim, ylim), data)
    x, y = np.float64(0.99), np.float64(0)

    # print(data)
    print(interp([x, y]))
    print(bilinear_interpolate(data, x, y))


if __name__ == '__main__':
    test_bilinear_interpolate()
