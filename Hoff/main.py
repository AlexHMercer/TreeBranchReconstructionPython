import os.path

from CircleCalculation import CircleCalculation
from print_data import print_position_radius
import sys
sys.setrecursionlimit(9000000)  # 这里设置大一些


def main():
    base_filename = "modelPlot2"
    target_directory = "../resource/" + base_filename + "_DBH/"
    tree_amount = 187

    for index in range(1, tree_amount):
        if not os.path.exists(target_directory):
            os.mkdir(target_directory)

        hoff = CircleCalculation(base_filename, target_directory, index)
        hoff.run()

        print_position_radius(target_directory, index)


if __name__ == "__main__":
    main()
