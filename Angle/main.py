from generateAngle import SearchTreeAndGenerateAngle
from printData import print_branches
from printData import print_angles
from AverageAngleDegree import AverageAngleDegree
from ParentPosition import ParentPosition


def main():
    # 应该是forwad_length从1开始，然后遍历到3，只要数据大于90度就进行更新（取最小），最后如果数据大于110，就判定为杂支，并把坐标输出
    start_index = 1
    end_index = 21
    for index in range(start_index, end_index):
        base_filename = "five_years"
        # base_filename = "C:/Users/Justinc/Desktop/大三下论文数据/draw_angles/resource/twenty_years"

        # 生成相应的角度数据 branches.data -> angles.data and angles.txt
        search = SearchTreeAndGenerateAngle(index, base_filename)
        search.run()

        # 由angles.data 生成 angles_full_info.txt
        print_angles(base_filename, index)

        # # 由branches.data 生成 branches.txt
        # print_branches(base_filename, index)

        # 由angles_full_info.txt生成一个excel统计表
        # 生成各个树的角度信息文件名为  xx_years_tree_full_angles.xlsx
        average_angle_degree = AverageAngleDegree(base_filename, index, end_index)
        average_angle_degree.run()

        position = ParentPosition(base_filename, index)
        position.run()
        position.out()


if __name__ == "__main__":
    main()
