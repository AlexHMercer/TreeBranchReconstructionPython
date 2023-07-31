import os.path
from matplotlib import pyplot as plt
import numpy as np
import pickle
from Branch import Branch
from numpy import sin, cos, sum, cross, arccos, linspace, pi, array
from numpy.linalg import norm
from my_lsq.lsq import lsq
import cv2
from db_scan import dbscan_filter


class CircleCalculation:
    R = 0.2  # 设置的超参数，应该是略大于数目的胸径比较合适
    Thick = 0.2  # 设置厚度的超参数，应该是步长的一般比骄傲合适
    iteration_length = 0
    cell_length = 1000  # 栅格设置为1000
    square_side_length = 0.6  # 设置为2m
    max_radius = 0.2  # 最大半径

    def __init__(self, base_filename, target_directory, index):
        CircleCalculation.iteration_length = 0  # 获取对应树的骨架文件和源文件路径
        filename = "../resource/" + base_filename + "_skeleton/tree" + str(index) + "/branches.data"
        original_filename = "../resource/" + base_filename + "/tree_" + str(index) + ".txt"

        self.target_directory = target_directory
        self.base_filename = base_filename
        self.branches = None
        self.index = index
        self.load_branch_data(filename) # 读取骨架文件
        self.root = None
        self.load_root_branch() # 读取骨架文件中被标记为root的branch节点
        self.original_data = None
        print("loading original data")
        self.load_original_data(original_filename)  # 读取树的原始点云文件
        print("load all needed data")
        self.create_folders()   # 创建该棵树的结果文件夹

    def create_folders(self):
        tree_folder = self.target_directory + "tree" + str(self.index) + "/"
        if not os.path.exists(tree_folder):
            os.mkdir(tree_folder)

        img_folder = tree_folder + "imgs/"
        if not os.path.exists(img_folder):
            os.mkdir(img_folder)

    def load_branch_data(self, branch_data):
        with open(branch_data, "rb") as f:
            self.branches = pickle.load(f)

    def load_root_branch(self):
        for branch in self.branches:
            if branch.is_root:
                self.root = branch
                # branch.parent_direction = np.array([0, 0, 1])
                break

    def load_original_data(self, original_filename: str):
        try:
            self.original_data = np.loadtxt(original_filename, delimiter="\t")[:, :3]
        except ValueError:
            try:
                self.original_data = np.loadtxt(original_filename, delimiter=" ")[:, :3]
            except ValueError:
                try:
                    self.original_data = np.loadtxt(original_filename, delimiter=",")[:, :3]
                except ValueError:
                    print("load point cloud data error, please check the file format")

    def run(self):
        root = self.root
        self._out(root, None)   # 为该branch节点确定半径
        self.duplicate_branches_data()  # 把self.branches写入Branches_c.data

    def _out(self, node: Branch, parent: Branch):
        CircleCalculation.iteration_length += 1 # iteration_length用来统计迭代次数
        print("iteration start: ", CircleCalculation.iteration_length)
        self._circle_calculation(node, parent) # 为节点确定半径约束，如果该节点没有父节点（即为根节点），则将半径约束设置为0.2m
        print("iteration end")

        children = node.children    # 为当前branch节点的所有子节点添加半径约束，约束长度是父节点的0.99倍
        for child in children:
            self._out(child, node)

    def _circle_calculation(self, node: Branch, parent: Branch):
        # 建模直径约束
        if parent is None:
            circle_radius = 0.2
        else:
            circle_radius = parent.radius * 0.99

        print("diameter is ", circle_radius * 2 * 100, "z ")
        node.radius = circle_radius

    def plt_circle(self, radius, center, x, y):
        center_x = center[0]
        center_y = center[1]
        plt.scatter(x, y)
        plt.scatter(center_x, center_y, c='r')
        theta = linspace(0, 2*pi, 1000)
        circle_x = center_x + cos(theta) * radius
        circle_y = center_y + sin(theta) * radius
        plt.plot(circle_x, circle_y)
        plt.axis('equal')
        filename = self.target_directory + "tree" + str(self.index) + "/imgs/" + str(CircleCalculation.iteration_length) + ".png"
        plt.savefig(filename)
        plt.close()

    @staticmethod
    def get_gray_img(x, y, center, id_1, id_2):
        # formula column = (x - original_x) // pixel + 50
        # formula line = (y - original_y) // pixel + 50
        cell_length = CircleCalculation.cell_length
        square_side_length = CircleCalculation.square_side_length

        xy_array = np.zeros((cell_length, cell_length))
        pixel = square_side_length / cell_length
        x_index = ((x - center[0]) // pixel + cell_length / 2).astype(int)
        y_index = ((y - center[1]) // pixel + cell_length / 2).astype(int)

        xy_array[x_index, y_index] = 255

        # xy_array *= 255
        # image = Image.fromarray(xy_array)
        # image = image.convert("L")
        # image = array(image)

        image = xy_array.astype(np.uint8)
        #  将其转化为cv2类型的图像，改变下数据类型即可

        # t = Image.fromarray(xy_array)
        # t = t.convert("L")
        # t.save("../resource/jiande_DBH/tree" + str(id_1) + "/imgs/t" + str(id_2) + ".png")
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # ret, thresh = cv2.threshold(image, 127, 255, 0)

        im2, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        out = list(list())
        for e in contours:
            out.append([e[0][0][0], e[0][0][1]])

        return array(out)

    def duplicate_branches_data(self):
        filename = self.target_directory + "tree" + str(self.index) + "/branches_c.data"
        # filename = "../hoff.data"
        with open(filename, "wb") as f:
            pickle.dump(self.branches, f)

    @staticmethod
    def get_rotation_matrix(v1, v2):
        nv1 = v1 / norm(v1)
        nv2 = v2 / norm(v2)

        if norm(nv1 + nv2) == 0:
            q = np.array([0, 0, 0, 0])
        else:
            if v1[0] == v2[0] and v1[1] == v2[1] and v1[2] == v2[2]:
                return np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            u = cross(nv1, nv2)
            u = u / norm(u)

            theta = arccos(sum(nv1 * nv2)) / 2
            q = np.array([cos(theta), sin(theta) * u[0], sin(theta) * u[1], sin(theta) * u[2]])

        q0 = q[0]
        q1 = q[1]
        q2 = q[2]
        q3 = q[3]

        l = [[1 - 2 * q2 ** 2 - 2 * q3 ** 2, 2 * q1 * q2 - 2 * q0 * q3, 2 * q1 * q3 + 2 * q0 * q2],
             [2 * q1 * q2 + 2 * q0 * q3, 1 - 2 * q1 ** 2 - 2 * q3 ** 2, 2 * q2 * q3 - 2 * q0 * q1],
             [2 * q1 * q3 - 2 * q0 * q2, 2 * q2 * q3 + 2 * q0 * q1, 1 - 2 * q1 ** 2 - 2 * q2 ** 2]]
        R = np.array(l)
        return R

    @staticmethod
    def get_radius(circles, pixel):
        max_radius = -float('inf')
        for circle in circles[0]:
            radius = circle[2] * pixel
            if radius > max_radius:
                max_radius = radius

        return max_radius


def main():
    # base_filename = "../resource/five_years"
    # index = 1
    # branch_data_filename = base_filename + "/tree" + str(index) + "/branches.data"
    # original_filename = "C:\\Users\\Justinc\\Desktop\\大三下论文数据\\原始数据txt\\five_years\\tree_000000.txt"
    #
    # hoff = CircleCalculation(branch_data_filename, original_filename)
    # hoff.run()
    print("This is test section, please run code in the main programmer")


if __name__ == "__main__":
    main()



#     def _circle_calculation(self, node: Branch, parent: Branch):
#         detected_points = list()
#
#         center = node.position
#         v = node.parent_direction
#         z = np.array([0, 0, 1])
#         R = CircleCalculation.get_rotation_matrix(v, z)
#
#         # if parent is None:
#         #     step = 1
#         # else:
#         #     step = max(CircleCalculation.R, CircleCalculation.Thick)
#         # top = center[2] + step
#         # bottom = center[2] - step
#         # points = self.original_data[self.original_data[:, 2] <= top, :]
#         # points = points[points[:, 2] >= bottom, :]
#
#         for point in self.original_data:
#             # 这个地方可以边遍历边删除，这样就可以减小循环的复杂度
#             # 距离约束
#             R_length = np.sqrt(np.sum((point - center) ** 2))
#             if R_length < CircleCalculation.R:
#                 t = point - center
#                 M_t = np.sqrt(np.sum(t ** 2))
#                 cos_t_v = np.abs(np.sum(t * z) / (np.sqrt(np.sum(t ** 2)) * np.sqrt(np.sum(z ** 2))))
#                 length = cos_t_v * M_t
#                 # print(length)
#                 # 角度约束
#                 if length < CircleCalculation.Thick / 2:
#                     detected_points.append(point)
#
#         # formula column = (x - original_x) // pixel + 50
#         # formula line = (y - original_y) // pixel + 50
#         xy_array = np.zeros((CircleCalculation.cell_length, CircleCalculation.cell_length))
#         transformed_original_x, transformed_original_y = np.dot(R, center)[:2]
#         pixel = CircleCalculation.square_side_length / CircleCalculation.cell_length
#         # trans_points = list()
#         # trans_points_txt = np.empty((0, 3))
#         for point in detected_points:
#             x, y = np.dot(R, point)[:2]
#
#             # line = np.array([x, y, point[2]])
#             # trans_points_txt = np.vstack((line, trans_points_txt))
#
#             column = int((x - transformed_original_x) // pixel + (CircleCalculation.cell_length / 2))
#             line = int((y - transformed_original_y) // pixel + (CircleCalculation.cell_length / 2))
#             # print(f"x is {x}, y is {y}, original x is {transformed_original_x}, original y is {transformed_original_y}")
#             # print(f"column is: {column}, line is {line}")
#             xy_array[line][column] = 1
#
#         # np.savetxt("./res/trans" + str(CircleCalculation.iteration_length) + ".txt", trans_points_txt, delimiter=",")
#
#         xy_array *= 255
#         x_y_image = Image.fromarray(xy_array)
#         x_y_image = x_y_image.convert("L")
#
#         image = np.array(x_y_image)
#
#         filename = self.target_directory + "tree" + str(self.index) + "/imgs/" + str(CircleCalculation.iteration_length) + ".png"
#         x_y_image.save(filename)
#
#
#         # start...........................................................
#         # # print(image)
#         # max_radius = int(CircleCalculation.max_radius // pixel)
#         # circles = HoughCircles(image, HOUGH_GRADIENT, 1, 40, param1=50, param2=9, minRadius=0, maxRadius=max_radius)
#         # # print("circle: ", circles)
#         #
#         # flag = True
#         # if circles is not None:
#         #     # if parent is None:
#         #     #     radius = CircleCalculation.get_radius(circles)
#         #     #     print("root radius is ", radius)
#         #     # else:
#         #     #     parent_radius = parent.radius
#         #     #     radius = CircleCalculation.get_radius(circles)
#         #     #     if not (parent_radius * 0.8) < radius < (parent_radius * 1.1):
#         #     #         for circle in circles[0]:
#         #     #             radius = circle[2] * pixel
#         #     #             # a < b / 2
#         #     #             if (parent_radius * 0.8) < radius < (parent_radius * 1.1):
#         #     #                 flag = False
#         #     #                 break
#         #     #         if flag:
#         #     #             radius = parent.radius * 0.98
#         #     radius = CircleCalculation.get_radius(circles, pixel)
#         # else:
#         #     if parent is None:
#         #         # radius = circles[0][2] * pixel
#         #         # print("root radius is ", radius, " and parent is None")
#         #         print("wrong" * 100)
#         #     else:
#         #         radius = parent.radius * 0.95
#         #
#         # print("diameter is ", radius * 2 * 100, "z ", center[2])
#         # node.radius = radius
#
#         # end...........................................................
#
#         (x, y), radius = minEnclosingCircle(image)
#         center = (int(x), int(y))
#         radius = int(radius) * pixel
#         print("diameter is ", radius * 2 * 100, "z ", center[2])
#         node.radius = radius
#
#         # cv2.circle(img, center, radius, (9, 255,), 2)