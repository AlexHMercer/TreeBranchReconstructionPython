import numpy as np


def main():
    out = np.empty((0, 3))

    for index in range(1, 21):
        base_filename = "five_years"
        filename = "../resource/" + base_filename + "_parent_position/" + str(index) + "_position.csv"
        print(index)
        data = np.loadtxt(filename, delimiter=",")[:, :3]
        out = np.vstack((out, data))
    out_filename = "../resource/" + base_filename + "_radar_angles.txt"

    np.savetxt(out_filename, out, delimiter=",")


if __name__ == "__main__":
    main()
