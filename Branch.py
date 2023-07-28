import numpy as np
from numpy.linalg import norm
from extratSkeleton.db_scan import dbscan_filter


class Branch:
    distance_of_nodes = 0.06

    def __init__(self, parent_direction, position):
        # all arguments are vector with three dimensions
        # parent: last node, position: current node, direction:__
        self.is_root = False  # 标记是不是根节点
        self.position = position  # 结点的坐标位置
        self.parent_direction = parent_direction  # 不存储父节点，而是存储父元素对自己的指向
        self.children = []  # 用于存储对应的子节点
        self.can_attracted = True
        self.attraction_points = []
        self.attraction_points_length = 0
        self.radius = 0

    def update_direction(self, leaf):
        self.attraction_points.append(leaf)
        self.attraction_points_length += 1

    def reset(self):
        self.attraction_points_length = 0
        self.attraction_points.clear()
        if len(self.children) == 2:
            self.can_attracted = False

    def next_branch(self):
        direction = self.parent_direction

        self.attraction_points = dbscan_filter(self.attraction_points)
        # 角度约束
        for i in range(len(self.attraction_points)-1, -1, -1):
            leaf = self.attraction_points[i]
            t = leaf.position - self.position
            numerator = np.sqrt(np.sum(t ** 2)) * np.sqrt(np.sum(direction ** 2))
            denominator = np.sum(t * direction)
            value = denominator / numerator
            if 0 <= value <= 1:  # 角度约束 0 - 90
                continue
            else:
                self.attraction_points.remove(leaf)

        if len(self.attraction_points) == 0:
            self.can_attracted = False
            return None

        direction_to_child = np.zeros(3)
        # 重新计算生长方向
        for leaf in self.attraction_points:
            new_direction = leaf.position - self.position
            new_direction = new_direction / norm(new_direction)
            direction_to_child += new_direction

        # normalize direction
        direction_to_child = direction_to_child / norm(direction_to_child)
        new_position = self.position + direction_to_child * Branch.distance_of_nodes

        new_branch = Branch(direction_to_child, new_position)
        print("new branch --- ", new_position)
        self.children.append(new_branch)
        self.reset()

        return new_branch
