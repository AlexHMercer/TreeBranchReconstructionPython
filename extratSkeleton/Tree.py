import os.path
import numpy as np
from numpy import cos, cross
from numpy.linalg import norm
from Branch import Branch
from Leaf import Leaf
import pickle

import sys
sys.setrecursionlimit(9000000)  # 这里设置大一些


class Tree:
    # tree 1
    # search_radius = 0.6
    # kill_radius = 0.4
    # kill_thick = 0.25

    # search_radius = 0.8
    # kill_radius = 0.35
    # kill_thick = 0.25

    # tree 3 tree 7
    search_radius = 1.3
    kill_radius = 0.6
    kill_thick = 0.25

    def __init__(self, base_filename, tree_id):
        self.branches_data_filename = None
        self.branches_txt_filename = None
        self.leaves_txt_filename = None
        self.branches = []
        self.leaves = []
        self.init(base_filename, tree_id)
        self.noise = []  # 存储最后的噪声点

    def run(self):
        run = True
        while run:
            run = False
            print("iteration start")

            # 设置初始条件，所有已存在的Branch还没有被任何Leaf吸引
            for branch in self.branches:
                branch.not_be_attracted = True

            # find branches needed to update 遍历所有剩余的点
            for leaf in self.leaves:
                d = float('inf')
                closest_branch = None # 距离当前点最近的Branch节点

                for branch in self.branches:
                    if branch.can_attracted:
                        distance = np.sqrt(np.sum((leaf.position - branch.position) ** 2)) # 计算当前Leaf点和Branch节点直接的距离
                        #  加入点，再改进
                        # if distance < Tree.radius and distance < d:  查找当前Leaf点在满足阈值的情况下，距离最近的Branch节点
                        if distance < Tree.search_radius and distance < d:
                            d = distance
                            closest_branch = branch
                            run = True
                # 如果存在这样的Branch，那么将吸附的点放入attraction_points中
                if closest_branch is not None:
                    closest_branch.not_be_attracted = False
                    closest_branch.update_direction(leaf)
# ------------------到这里，对所有Leaf的一次遍历已经结束了-------------------------------------------
            # 过滤无用点，如果在一次迭代中，生成点没有被吸引，那么以后也不会被吸引
            for branch in self.branches:
                if branch.not_be_attracted:
                    branch.can_attracted = False

            # update branched and kill points
            if run:
                for branch in self.branches:
                    if branch.attraction_points_length > 0:  # 如果当前Branch吸附的点的数量>0
                        new_branch: Branch = branch.next_branch(self.noise)  # 根据吸附的点和噪点生成新的Branch节点
                        if new_branch is not None:
                            self.branches.append(new_branch)
                            kill_radius = Tree.kill_radius
                            kill_thick = Tree.kill_thick
                            # delete leaves
                            for leaf in self.leaves:
                                # branch_center = new_branch.position
                                # branch_direction = new_branch.parent_direction
                                # direction = leaf.position - branch_center
                                #
                                # thick = np.abs(np.sum(branch_direction * direction)) / norm(branch_direction)
                                # radius = np.abs(norm(cross(branch_direction, direction))) / norm(branch_direction)

                                # if thick < kill_thick and radius < kill_radius:
                                # 删除点 把新Branch节点周围的Leaf点去除
                                distance = np.sqrt(np.sum((leaf.position - new_branch.position) ** 2))
                                # print("dis: ", distance)
                                if distance < Tree.kill_radius:
                                    self.leaves.remove(leaf)

            leaves_length = len(self.leaves)
            branches_length = len(self.branches)
            print("Leaves length is ", leaves_length)
            print("Branches length is ", branches_length)
            print("Next calculation amount is about", leaves_length * branches_length)
            print("iteration end")

        self.save_data(1, 1)

    def init(self, base_filename, tree_id):
        target_directory = "../resource/" + base_filename + "_skeleton/tree" + str(tree_id) + "/"
        self.branches_data_filename = target_directory + "branches.data"
        self.branches_txt_filename = target_directory + "branches.txt"
        self.leaves_txt_filename = target_directory + "leaves.txt"

        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        original_tree_name = "../resource/" + base_filename + "/tree_" + str(tree_id) + ".txt"

        # 读取点云文件
        try:
            points = np.loadtxt(original_tree_name, delimiter="\t")[:, :3]

        except ValueError:
            try:
                points = np.loadtxt(original_tree_name, delimiter=" ")[:, :3]
            except ValueError:
                try:
                    points = np.loadtxt(original_tree_name, delimiter=";")[:, :3]
                except ValueError:
                    print("extract tree skeleton: load point cloud data error, please check the file format")
        # 找到z轴的最小值对应的点的xy值
        z_value_min = min(points[:, 2])
        x_y_value = points[points[:, 2] == z_value_min, :2]
        x_y_value = np.squeeze(x_y_value)

        parent_direction = np.array([0, 0, 1])
        if x_y_value.size == 2:
            position = np.array([x_y_value[0], x_y_value[1], z_value_min - 1e-5])
        else:
            position = np.array([x_y_value[0][0], x_y_value[0][1], z_value_min - 1e-5])

        print(f"root position: ", position)
        # 生成一个类型为Branch的节点，并将其作为根节点
        root: Branch = Branch(parent_direction, position)
        root.is_root = True
        # 整个树由多个Branch组成，存储于branches中
        self.branches.append(root)
        # 遍历每一个点，并将其坐标封装为Leaf类放入Tree的leaves集合中
        for point in points:
            self.leaves.append(Leaf(point))

    def save_data(self, signum, frame):
        with open(self.branches_data_filename, "wb") as f:
            pickle.dump(self.branches, f)

        out = np.empty((0, 3))
        for branch in self.branches:
            out = np.vstack((out, branch.position))
        np.savetxt(self.branches_txt_filename, out, delimiter=',')

        out = np.empty((0, 3))
        for leaf in self.leaves:
            out = np.vstack((out, leaf.position))

        print("noise length is: ", len(self.noise))
        for leaf in self.noise:
            out = np.vstack((out, leaf.position))

        np.savetxt(self.leaves_txt_filename, out, delimiter=',')
