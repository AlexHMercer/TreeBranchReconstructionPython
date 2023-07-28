from scipy.optimize import leastsq
from numpy import sqrt, square, sin, cos


def residual_func(center, x, y):
    center_x = center[0]
    center_y = center[1]
    R = sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    return square((R - R.mean()))


def lsq(center, x, y):
    try:
        o_center, _ = leastsq(residual_func, center, args=(x, y))
        center_x = center[0]
        center_y = center[1]
        o_r = sqrt((x - center_x) ** 2 + (y - center_y) ** 2).mean()
    except TypeError:
        o_center = None
        o_r = None
    return o_center, o_r


