import os.path

from numpy import loadtxt, savetxt, sum, empty, vstack, median, linspace, pi, sin, cos, mean
from utils.Load import load_cloud
from matplotlib import pyplot as plt


def main():
    base_filename = "jiande"
    original_filename = "../resource/tree_DBH_index.txt"
    original = loadtxt(original_filename, delimiter="\t")
    lidar_filename = "../resource/tree_DBH_index_lidar.txt"
    lidar = loadtxt(lidar_filename, delimiter="\t")

    number = 104
    x_bottom = -0.15
    x_top = 0.15
    y_bottom = -0.15
    y_top = 0.15
    z_position = 1.3
    scale = 0.1

    svg_out_directory = "../resource/" + base_filename + "_tree_svg/"
    if not os.path.exists(svg_out_directory):
        os.mkdir(svg_out_directory)

    mapper = dict()

    for index in range(1, number):
        mapper[index] = list()
        original_tree_filename = "../resource/" + base_filename + "/tree_" + str(index) + ".txt"

        filename = "../resource/" + base_filename + "_DBH/tree" + str(index) + "/circles" + str(index) + ".txt"
        tree_circle = loadtxt(filename, delimiter=',')
        z_top = z_position + scale
        z_bottom = z_position - scale
        tree_circle = tree_circle[tree_circle[:, 3] <= z_top, :]
        tree_circle = tree_circle[tree_circle[:, 3] >= z_bottom, :3]

        center_x = median(tree_circle[:, 1])
        center_y = median(tree_circle[:, 2])

        # radius = median(tree_circle[:, 0])

        radius = mean(tree_circle[:, 0])

        # circles_length = len(circles)
        #
        # out = sum(circles) / circles_length
        # 截取相应的数据
        original_tree = load_cloud(original_tree_filename)

        clouds = original_tree[original_tree[:, 2] >= z_bottom]
        clouds = clouds[clouds[:, 2] <= z_top]
        clouds = clouds[:, :2]

        # if clouds.shape[0] != 0:
        #     clouds = dbscan_filter(clouds, min_samples=20)

        theta = linspace(0, 2*pi, 1000)
        x = cos(theta) * radius
        y = sin(theta) * radius

        fig = plt.figure(figsize=(3, 3))
        fig.add_axes([0, 0, 1, 1])
        plt.scatter(clouds[:, 0] - center_x, clouds[:, 1] - center_y)
        plt.plot(x, y)
        plt.axis('equal')
        plt.axis('square')
        plt.xlim([x_bottom, x_top])
        plt.ylim([y_bottom, y_top])

        plt.axis('off')
        plt.xticks([])
        plt.yticks([])

        plt.savefig(svg_out_directory + str(index) + '.png', format='png', dpi=150)  # 输出
        plt.close()

        mapper[index].append(radius * 2 * 100)

    print(mapper)

    for line in original:
        index = int(line[0])

        original_diameter = line[1] * 100
        mapper[index].append(original_diameter)

    for index, value in enumerate(lidar):
        lidar_diameter = value * 100
        mapper[index+1].append(lidar_diameter)

    out = empty((0, 5))
    for key, value in mapper.items():
        # 真实，测量 测量误差 lidar lidar误差
        true = value[1]
        ours = value[0]
        lidar = value[2]
        ours_error = abs(ours - true) / true
        lidar_error = abs(lidar - true) / true
        line = [true, ours, ours_error, lidar, lidar_error]
        out = vstack((out, line))

    savetxt("../resource/comparison.csv", out, delimiter=",", fmt='%f')


if __name__ == "__main__":
    main()
