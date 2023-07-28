from numpy.linalg import norm
import numpy as np
from extratSkeleton.db_scan import dbscan_filter


class Branch:
    distance_of_nodes = 0.1

    def __init__(self, parent_direction, position):
        # all arguments are vector with three dimensions
        # parent: last node, position: current node, direction:__

        # 这里的can_attracted和not_be_attracted用于减少每次遍历的次数，每次迭代开始时，can_attracted默认为True
        # 所有Branch的not_be_attracted置为true，表示没有被任何节点吸引，在所有的Leaf点都遍历完成后，
        # 如果有的Branch的not_be_attracted依旧为true，说明这个Branch阈值的周围没有点，所以在下次遍历的时候就不需要遍历这个Branch
        # 将can_attracted置为false
        self.is_root = False  # 标记是不是根节点
        self.position = position  # 结点的坐标位置
        self.parent_direction = parent_direction  # 不存储父节点，而是存储父元素对自己的指向，即父节点到当前节点的向量
        self.children = []  # 用于存储对应的子节点
        self.can_attracted = True
        self.attraction_points = []
        self.attraction_points_length = 0
        self.not_be_attracted = True
        self.radius = 0

    def update_direction(self, leaf):
        self.attraction_points.append(leaf)
        self.attraction_points_length += 1

    def reset(self):
        self.attraction_points_length = 0
        self.attraction_points.clear()
        if len(self.children) == 2:  # 一个节点最多只能有两个子节点
            self.can_attracted = False

    def next_branch(self, noise):
        direction = self.parent_direction  # direction是当前Branch节点的父节点

        self.attraction_points = dbscan_filter(self.attraction_points, noise)

        # 角度约束
        for i in range(len(self.attraction_points)-1, -1, -1):
            leaf = self.attraction_points[i]
            t = leaf.position - self.position
            numerator = np.sqrt(np.sum(t ** 2)) * np.sqrt(np.sum(direction ** 2))
            denominator = np.sum(t * direction)
            value = denominator / numerator  # 以上求两向量夹角的cos值，一个向量是原点指向当前Branch节点的父节点，另一个向量是当前Branch节点指向当前遍历的Leaf节点
            if 0 <= value <= 1:  # 角度约束 0 - 90，cosα不在0-1之间的从吸附的点中去除
                continue
            else:
                self.attraction_points.remove(leaf)
        # 若所有的之前获取的已吸附的点均不满足上述角度约束，则该Branch节点没有后继Branch节点
        if len(self.attraction_points) == 0:
            self.can_attracted = False
            self.reset()
            return None
        # 这里就是计算下一个Branch节点的self.parent_direction属性，即经过归一化的当前Branch到子Branch的向量
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
