from numpy import loadtxt, savetxt, empty, vstack
from utils.Load import load_cloud

def main():
    base_filename = "jiande"

    directory = "../resource/" + base_filename + "_skeleton/"
    target_directory = "../resource/" + base_filename + "/"
    tree_amount = 104

    for index in range(1, tree_amount):
        noise_filename = directory + "tree" + str(index) + "/leaves.txt"
        tree_filename = target_directory + "tree_" + str(index) + ".txt"
        out = empty((0, 3))
        noise = load_cloud(noise_filename)
        tree = load_cloud(tree_filename)

        for line_tree in tree:
            flag = True
            for line_noise in noise:
                if line_tree[0] == line_noise[0] and line_tree[0] == line_noise[0] and line_tree[0] == line_noise[0]:
                    flag = False
                    break
            if flag:
                out = vstack((out, line_tree[:3]))

        savetxt(tree_filename, out, delimiter=",")
        print(index)


if __name__ == "__main__":
    main()
