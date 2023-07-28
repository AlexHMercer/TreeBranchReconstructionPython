import os.path
from numpy import empty, vstack, savetxt
from Branch import Branch as Branch1
from extratSkeleton.Branch import Branch as Branch2
import pickle
import sys
import numpy as np
sys.setrecursionlimit(9000000)  # 这里设置大一些


def recurve(node, parent: Branch2, l: list):
    parent_direction = node.parent_direction
    position = node.position
    children = node.children

    branch = Branch2(parent_direction, position)
    if parent_direction is None:
        print("wrong" * 100)

    l.append(branch)
    parent.children.append(branch)

    for child in children:
        recurve(child, branch, l)


def main():
    base_filename = "test"

    if not os.path.exists("./resource/" + base_filename + "_skeleton/"):
        os.mkdir("./resource/" + base_filename + "_skeleton/")

    for tree_id in range(1, 2):
        filename = "./resource/" + base_filename + "/tree_" + str(tree_id) + ".txt"
        with open(filename, "rb") as f:
            branches = pickle.load(f)

        l = list()


        root_o = branches[0]
        position = root_o.position
        parent_direction = root_o.parent_direction
        if parent_direction is None:
            print("start")
        else:
            print("wrong" * 100)

        parent_direction = np.array([0, 0, 1])
        root = Branch2(parent_direction, position)
        root.is_root = True

        l.append(root)

        for child in root_o.children:
            recurve(child, root, l)

        directory = "./resource/" + base_filename + "_skeleton/tree" + str(tree_id) + "/"
        if not os.path.exists(directory):
            os.mkdir(directory)

        print(len(l))
        filename = directory + "branches.data"
        with open(filename, "wb") as f:
            pickle.dump(l, f)

        with open(filename, "rb") as f:
            branches = pickle.load(f)

        out = empty((0, 3))
        for branch in branches:
            out = vstack((out, branch.position))
        filename = directory + "branches.txt"
        savetxt(filename, out, delimiter=",")

        out = empty((0, 6))
        for branch in branches:
            for child in branch.children:
                line = []
                line.extend(branch.position)
                line.extend(child.position)
                out = vstack((out, line))

        filename = directory + "relationship.txt"
        savetxt(filename, out, delimiter=",")


if __name__ == "__main__":
    main()


