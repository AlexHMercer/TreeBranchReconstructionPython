import numpy as np
import pickle


def print_angles(base_filename, index):
    out_filename = "../resource/" + base_filename + "_angles/" + str(index) + "_angles_full_info.txt"
    filename = "../resource/" + base_filename + "_angles/" + str(index) + "_angles.data"

    with open(filename, "rb") as f:
        angles = pickle.load(f)

    out = np.empty((0, 19))

    for angle in angles:
        line = []
        line.extend(angle.parent_position)
        line.extend(angle.children1_position)
        line.extend(angle.children2_position)
        line.extend(angle.parent_direction)
        line.extend(angle.children1_direction)
        line.extend(angle.children2_direction)
        line.append(angle.branch_level)

        # print(line)
        out = np.vstack((out, line))
    np.savetxt(out_filename, out, delimiter=",")


def print_branches(base_filename, index):
    out_filename = base_filename + "_angles/" + str(index) + "_branches.txt"
    filename = base_filename + "/tree" + str(index+1) + "/branches.data"

    with open(filename, "rb") as f:
        branches = pickle.load(f)

    out = np.empty((0, 6))
    for branch in branches:
        children = branch.children
        for child in children:
            line = []
            line.extend(branch.position)
            line.extend(child.position)
            out = np.vstack((out, line))

    np.savetxt(out_filename, out, delimiter=",")


def main():
    for index in range(20):
        filename = "./five_years_angles/" + str(index) + "_angles.data"
        print_angles(filename, index)

    for index in range(20):
        filename = "./five years/tree" + str(index+1) + "/branches.data"
        print_branches(filename, index)


if __name__ == "__main__":
    main()

