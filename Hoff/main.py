import os.path

from CircleCalculation import CircleCalculation
from print_data import print_position_radius
import sys
sys.setrecursionlimit(9000000)  # 这里设置大一些


def main():
    # 定义存放结果文件的路径，与要处理的文件个数
    base_filename = "test"
    target_directory = "../resource/" + base_filename + "_DBH/"
    tree_amount = 187

    for index in range(7, 8):
        if not os.path.exists(target_directory):
            os.mkdir(target_directory)

        hoff = CircleCalculation(base_filename, target_directory, index)
        hoff.run()

        print_position_radius(target_directory, index)


if __name__ == "__main__":
    main()
