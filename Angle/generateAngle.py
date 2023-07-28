import os.path
import pickle
import numpy as np
from Angle import Angle


class SearchTreeAndGenerateAngle:
    forward_length = 3

    def __init__(self, tree_id, base_filename):
        self.tree_id = tree_id
        self.filename = "../resource/" + base_filename + "_angles/"
        filename = "../resource/" + base_filename + "_skeleton/tree" + str(tree_id) + "/branches.data"
        if not os.path.exists(self.filename):
            os.mkdir(self.filename)

        with open(filename, "rb") as f:
            self.branches = pickle.load(f)
        self.angles = []

    def run(self):
        for branch in self.branches:
            # if branch.root_flag:
                print("start from point with: ", branch.position)
                self.search(branch, branch_level=1)
                self.save_angles()
                self.out()
                break

    def search(self, startpoint, branch_level=None):
        next_point = startpoint
        if branch_level == 1:
            v0 = np.array([0, 0, 1])
        else:
            v0 = next_point.parent_direction

        while True:
            children = next_point.children

            length = len(children)
            if length == 0:
                return
            elif length == 1:
                next_point = children[0]
                v0 = next_point.parent_direction
            else:
                # 下面最多处理一个点出现三个分支的情况，如果多的话就认定为多余的杂枝
                break

        if length == 2:
            child1 = children[0]
            child2 = children[1]
            child1_can_forward = self.can_forward(child1)
            child2_can_forward = self.can_forward(child2)

            if child1_can_forward is not True and child2_can_forward is not True:
                return
            elif child1_can_forward is True and child2_can_forward is not True:
                self.search(child1, branch_level)
                return
            elif child1_can_forward is not True and child2_can_forward is True:
                self.search(child2, branch_level)
                return

            v1 = child1.parent_direction
            v2 = child2.parent_direction
            cos1 = np.sum(v0*v1) / (np.sqrt(np.sum(v0**2)) * np.sqrt(np.sum(v1**2)))
            cos2 = np.sum(v0*v2) / (np.sqrt(np.sum(v0**2)) * np.sqrt(np.sum(v2**2)))

            v1 = self.reset(child1)
            v2 = self.reset(child2)

            angle = Angle(next_point.position, child1.position, child2.position, v0, v1, v2, branch_level)
            self.angles.append(angle)

            if cos1 < cos2:  # v0和v1之间的夹角更大，v1是子分支
                self.search(child1, branch_level+1)
                self.search(child2, branch_level)
            else:
                self.search(child2, branch_level+1)
                self.search(child1, branch_level)

        elif length == 3:
            child1 = children[0]
            child2 = children[1]
            child3 = children[2]

            child1_can_forward = self.can_forward(child1)
            child2_can_forward = self.can_forward(child2)
            child3_can_forward = self.can_forward(child3)

            v1 = child1.parent_direction
            v2 = child2.parent_direction
            v3 = child3.parent_direction

            cos1 = np.sum(v0 * v1) / (np.sqrt(np.sum(v0 ** 2)) * np.sqrt(np.sum(v1 ** 2)))
            cos2 = np.sum(v0 * v2) / (np.sqrt(np.sum(v0 ** 2)) * np.sqrt(np.sum(v2 ** 2)))
            cos3 = np.sum(v0 * v3) / (np.sqrt(np.sum(v0 ** 2)) * np.sqrt(np.sum(v3 ** 2)))



            if child3_can_forward and child2_can_forward and child1_can_forward:

                v1 = self.reset(child1)
                v2 = self.reset(child2)
                v3 = self.reset(child3)

                max_value = min(cos1, cos2, cos3)
                if cos1 == max_value:
                    angle1 = Angle(next_point.position, child1.position, child2.position, v0, v1, v2, branch_level)
                    angle2 = Angle(next_point.position, child1.position, child3.position, v0, v1, v3, branch_level)
                    self.angles.append(angle1)
                    self.angles.append(angle2)
                    self.search(child1, branch_level)
                    self.search(child2, branch_level+1)
                    self.search(child3, branch_level+1)
                elif cos2 == max_value:
                    angle1 = Angle(next_point.position, child2.position, child1.position, v0, v2, v1, branch_level)
                    angle2 = Angle(next_point.position, child2.position, child3.position, v0, v2, v3, branch_level)
                    self.angles.append(angle1)
                    self.angles.append(angle2)
                    self.search(child2, branch_level)
                    self.search(child1, branch_level+1)
                    self.search(child3, branch_level+1)
                elif cos3 == max_value:
                    angle1 = Angle(next_point.position, child3.position, child1.position, v0, v3, v1, branch_level)
                    angle2 = Angle(next_point.position, child3.position, child2.position, v0, v3, v2, branch_level)
                    self.angles.append(angle1)
                    self.angles.append(angle2)
                    self.search(child3, branch_level)
                    self.search(child2, branch_level+1)
                    self.search(child1, branch_level+1)

            elif child3_can_forward and child2_can_forward and not child1_can_forward:
                v2 = self.reset(child2)
                v3 = self.reset(child3)

                angle = Angle(next_point.position, child2.position, child3.position, v0, v2, v3, branch_level)
                self.angles.append(angle)

                if cos3 < cos2:  # v0和v1之间的夹角更大，v1是子分支
                    self.search(child3, branch_level + 1)
                    self.search(child2, branch_level)
                else:
                    self.search(child2, branch_level + 1)
                    self.search(child3, branch_level)

            elif child3_can_forward and not child2_can_forward and child1_can_forward:

                v1 = self.reset(child1)
                v3 = self.reset(child3)

                angle = Angle(next_point.position, child1.position, child3.position, v0, v1, v3, branch_level)
                self.angles.append(angle)

                if cos3 < cos1:  # v0和v1之间的夹角更大，v1是子分支
                    self.search(child3, branch_level + 1)
                    self.search(child1, branch_level)
                else:
                    self.search(child1, branch_level + 1)
                    self.search(child3, branch_level)

            elif not child3_can_forward and child2_can_forward and child1_can_forward:
                v1 = self.reset(child1)
                v2 = self.reset(child2)

                angle = Angle(next_point.position, child1.position, child2.position, v0, v1, v2, branch_level)
                self.angles.append(angle)

                if cos1 < cos2:  # v0和v1之间的夹角更大，v1是子分支
                    self.search(child1, branch_level + 1)
                    self.search(child2, branch_level)
                else:
                    self.search(child2, branch_level + 1)
                    self.search(child1, branch_level)

            elif child3_can_forward and not child2_can_forward and not child1_can_forward:
                self.search(child3, branch_level)

            elif not child3_can_forward and child2_can_forward and not child1_can_forward:
                self.search(child2, branch_level)

            elif not child3_can_forward and not child2_can_forward and child1_can_forward:
                self.search(child1, branch_level)
            else:
                return

    def save_angles(self):
        filename = self.filename + str(self.tree_id) + "_angles.data"
        # print("save angles")
        # print(filename)
        with open(filename, "wb") as f:
            pickle.dump(self.angles, f)

    def out(self):
        filename = self.filename + str(self.tree_id) + "_angles.txt"
        out = np.empty((0, 3))
        for angle in self.angles:
            out = np.vstack((out, angle.parent_position))
            out = np.vstack((out, angle.children1_position))
            out = np.vstack((out, angle.children2_position))

        np.savetxt(filename, out, delimiter=",")

    def reset(self, child):
        v = child.parent_direction
        node = child

        for i in range(SearchTreeAndGenerateAngle.forward_length):
            children = node.children

            if len(children) == 2:
                child1 = children[0]
                child2 = children[1]

                v1 = child1.parent_direction
                v2 = child2.parent_direction
                cos1 = np.sum(v * v1) / (np.sqrt(np.sum(v ** 2)) * np.sqrt(np.sum(v1 ** 2)))
                cos2 = np.sum(v * v2) / (np.sqrt(np.sum(v ** 2)) * np.sqrt(np.sum(v2 ** 2)))
                if cos1 < cos2:
                    node = child2
                    v = v2
                else:
                    node = child1
                    v = v1

            elif len(children) == 3:
                child1 = children[0]
                child2 = children[1]
                child3 = children[2]

                v1 = child1.parent_direction
                v2 = child2.parent_direction
                v3 = child3.parent_direction

                cos1 = np.sum(v * v1) / (np.sqrt(np.sum(v ** 2)) * np.sqrt(np.sum(v1 ** 2)))
                cos2 = np.sum(v * v2) / (np.sqrt(np.sum(v ** 2)) * np.sqrt(np.sum(v2 ** 2)))
                cos3 = np.sum(v * v3) / (np.sqrt(np.sum(v ** 2)) * np.sqrt(np.sum(v3 ** 2)))

                max_value = min(cos1, cos2, cos3)
                if cos1 == max_value:
                    node = child1
                    v = v1
                elif cos2 == max_value:
                    node = child2
                    v = v3
                elif cos3 == max_value:
                    node = child3
                    v = v3
            else:
                node = children[0]
                v = node.parent_direction

        return v

    def can_forward(self, branch):
        counter = 0
        next_node = branch
        while True:
            if counter == SearchTreeAndGenerateAngle.forward_length:
                break

            children = next_node.children
            if len(children) == 0:
                break

            if len(children) == 2:
                child1 = children[0]
                child2 = children[1]

                v = next_node.parent_direction
                v1 = child1.parent_direction
                v2 = child2.parent_direction
                cos1 = np.sum(v * v1) / (np.sqrt(np.sum(v ** 2)) * np.sqrt(np.sum(v1 ** 2)))
                cos2 = np.sum(v * v2) / (np.sqrt(np.sum(v ** 2)) * np.sqrt(np.sum(v2 ** 2)))
                if cos1 < cos2:
                    next_node = child2
                else:
                    next_node = child1
                counter += 1
            elif len(children) == 3:
                child1 = children[0]
                child2 = children[1]
                child3 = children[2]

                v = next_node.parent_direction
                v1 = child1.parent_direction
                v2 = child2.parent_direction
                v3 = child3.parent_direction

                cos1 = np.sum(v * v1) / (np.sqrt(np.sum(v ** 2)) * np.sqrt(np.sum(v1 ** 2)))
                cos2 = np.sum(v * v2) / (np.sqrt(np.sum(v ** 2)) * np.sqrt(np.sum(v2 ** 2)))
                cos3 = np.sum(v * v3) / (np.sqrt(np.sum(v ** 2)) * np.sqrt(np.sum(v3 ** 2)))

                max_value = min(cos1, cos2, cos3)
                if cos1 == max_value:
                    next_node = next_node.children[0]
                    counter += 1
                elif cos2 == max_value:
                    next_node = next_node.children[1]
                    counter += 1
                elif cos3 == max_value:
                    next_node = next_node.children[2]
                    counter += 1
            else:
                next_node = next_node.children[0]
                counter += 1

        if counter == SearchTreeAndGenerateAngle.forward_length:
            return True
        else:
            return False


def main():
    for index in range(20):
        # base_filename = "./five years/tree" + str(index+1) + "/branches.data"
        base_filename = "../resource/five_years"
        search = SearchTreeAndGenerateAngle(index, base_filename)
        search.run()


if __name__ == "__main__":
    main()
