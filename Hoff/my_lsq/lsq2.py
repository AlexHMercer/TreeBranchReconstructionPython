from scipy.optimize import leastsq
from numpy import sqrt, square, sin, cos


def residual_func2(radius, center, x, y):
    center_x = center[0]
    center_y = center[1]
    R = (sqrt((x - center_x) ** 2 + (y - center_y) ** 2) - radius)
    return R


def lsq2(center, x, y):
    radius = 0
    radius, _ = leastsq(residual_func2, radius, args=(center, x, y))
    return radius


