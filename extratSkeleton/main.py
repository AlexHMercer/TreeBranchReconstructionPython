from Tree import Tree

'''
    总结：
    1. 将z坐标的最小值作为起始Branch节点
    2. 遍历所有的Leaf（初始就是所有点云的坐标）节点，对每一个Leaf节点，找符合条件且距离最近的Branch节点，
       并将当前Leaf加入找到的Branch的吸附集合中。
    3. 再遍历所有的Branch，若吸附集合不为空，则根据吸附的点，和父节点向量，确定下一个Branch节点的坐标，同时要满足角度约束
    4. 对创建的新节点，根据定义的阈值，将节点周围距离小于阈值的Leaf从总集合中删去，加快下次遍历的速度。
'''
def main():
    base_filename = "test"
    # tree_[index].txt
    for index in range(7, 8):
        tree = Tree(base_filename, index) # 创建了Tree，并将最底部的点封装为Branch，并令为rootBranch，将所有的点坐标封装为Leaf
        tree.run()


if __name__ == "__main__":
    main()
