import pickle
import numpy as np
from numpy import vstack, hstack
from numpy import array, empty, zeros, ones


def print_position_radius(target_directory, index):
    filename = target_directory + "tree" + str(index) + "/branches_c.data"

    with open(filename, "rb") as f:
        branches = pickle.load(f)

    out = empty((0, 7))
    for branch in branches:
        line = list()
        line.append(branch.radius)
        line.extend(branch.position)
        line.extend(branch.parent_direction)  # line is instance of list, direction is instance of numpy.ndarray
        out = vstack((out, line))

    out_branches_filename = target_directory + "tree" + str(index) + "/circles" + str(index) + ".txt"
    np.savetxt(out_branches_filename, out, delimiter=",")

    out = empty((0, 8))
    for branch in branches:
        children = branch.children
        for child in children:
            line = []
            line.append(branch.radius)
            line.extend(branch.position)
            line.append(child.radius)
            line.extend(child.position)
            out = np.vstack((out, line))

    radius_infos = target_directory + "tree" + str(index) + "/radius_infos" + str(index) + ".txt"
    np.savetxt(radius_infos, out, delimiter=",")

    out = empty((0, 6))
    for branch in branches:
        children = branch.children
        for child in children:
            line = []
            line.extend(branch.position)
            line.extend(child.position)
            out = np.vstack((out, line))

    relationship = target_directory + "tree" + str(index) + "/relationship" + str(index) + ".txt"
    np.savetxt(relationship, out, delimiter=",")





