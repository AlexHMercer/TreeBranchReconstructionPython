import os.path
import pickle
import numpy as np


class ParentPosition:
    # 这里做的是一棵树对应一个文件
    def __init__(self, base_filename, index):
        filename = "../resource/" + base_filename + "_angles/" + str(index) + "_angles.data"
        original_filename = "../resource/" + base_filename + "_skeleton/tree" + str(index) + "/" + "branches.txt"
        out_filename = "../resource/" + base_filename + "_parent_position/" + str(index) + "_position.csv"

        if not os.path.exists("../resource/" + base_filename + "_parent_position/"):
            os.mkdir("../resource/" + base_filename + "_parent_position/")

        self.out_view_filename = "../resource/" + base_filename + "_parent_position/" + str(index) + "_view.txt"

        self.angles = np.empty((0, 3), dtype=float)
        self.load_angles(filename)

        self.origin = None
        self.load_tree_center(original_filename)

        # original_tree 是用来获取树的原点坐标
        self.file = None
        self.create_file(out_filename)
        self.direction = np.array([1, 0])

    def load_angles(self, angle_data):
        with open(angle_data, "rb") as f:
            angles = pickle.load(f)

        angles_list = []
        for angle in angles:
            line = angle.parent_position[:2]
            d1 = angle.children1_direction
            d2 = angle.children2_direction
            denominator = np.sqrt(np.sum(d1**2)) * np.sqrt(np.sum(d2**2))
            numerator = np.sum(d1*d2)
            cos_value = numerator / denominator
            line = np.hstack((line, cos_value))
            angles_list.append(line)

        for index in range(len(angles_list)-1, -1, -1):
            value = angles_list[index]
            is_repetitive = False
            counter = 0
            for angle in angles_list:
                if angle[0] == value[0] and angle[1] == value[1]:
                    counter += 1
                    if counter == 2:
                        is_repetitive = True
                        break
            if is_repetitive:
                angles_list.pop(index)
                print(value)

        for angle in angles_list:
            self.angles = np.vstack((self.angles, np.array(angle)))

    # 这个还要优化
    def load_tree_center(self, original_tree):
        points = np.loadtxt(original_tree, delimiter=",")[:, :3]
        z_value_min = min(points[:, 2])
        # print(z_value_min)
        x_y_value = points[points[:, 2] == z_value_min, :2]
        x_y_value = np.squeeze(x_y_value)

        if x_y_value.size == 2:
            self.origin = np.array(x_y_value)
        else:
            self.origin = np.array([x_y_value[0][0], x_y_value[0][1]])

        # print(self.origin)
        # self.origin = np.array([14.647, -21.304])

    def create_file(self, filename):
        self.file = open(filename, "w")
        # self.file.write("length,degree\r\n")

    def out(self):
        # print(self.angles.shape)
        out = np.hstack((self.angles[:, :2], np.ones((self.angles.shape[0], 1))))
        np.savetxt(self.out_view_filename, out, delimiter=",")

    def run(self):
        for angle in self.angles:
            line = ""
            distance = np.sqrt(np.sum((angle[:2] - self.origin)**2))
            direction = angle[:2] - self.origin
            degree = np.sum(direction * self.direction) / (np.sqrt(np.sum(direction**2)) * np.sqrt(np.sum(self.direction**2)))
            degree = np.arccos(degree)
            # line += str(distance) + "," + str(np.arccos(degree)/np.pi*180) + "\n"
            if angle[1] < self.origin[1]:
                degree = 2*np.pi - degree

            tree_angle = angle[2]
            line += str(degree) + "," + str(distance) + "," + str(tree_angle) + "\n"
            # print(line)
            self.file.write(line)
        self.file.close()


def main():
    base_filename = "twenty_years"
    for index in range(1, 21):
        position = ParentPosition(base_filename, index)
        position.run()
        position.out()


if __name__ == "__main__":
    main()
