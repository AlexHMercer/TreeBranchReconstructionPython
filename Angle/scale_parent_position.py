import numpy as np


def main(index):
    segment_length = 3
    target = [0.46, 0.6]
    original = [0, 0.25, 1]

    filename = "twenty_years_parent_position/" + str(index) + "_position.csv"
    out_filename = "twenty_years_parent_position/" + str(index) + "_scale_position.csv"

    data = np.loadtxt(filename, delimiter=",")
    degrees = data[:, 0]
    lengths = data[:, 1]
    max_length = max(lengths)
    tree_angles = data[:, 2]

    scale = list()
    for index in range(len(target)):
        scale.append(target[index] / (original[index + 1] - original[index]))

    original_department = list()
    for index in range(len(original)):
        original_department.append(max_length * original[index])

    # print(original_department)

    target_department = list()
    target_department.append(0)
    t = 0
    for index in range(len(target)):
        t += target[index]
        target_department.append(t * max_length)

    tmp = lengths.copy()
    # 分成四段
    for i in range(segment_length):
        for index in range(len(tmp)):
            length = tmp[index]
            # print(i)
            if original_department[i] < length < original_department[i + 1]:
                lengths[index] = (length - original_department[i]) * scale[i] + target_department[i]

    lengths = np.expand_dims(lengths, 1)
    print(lengths.shape)
    degrees = np.expand_dims(degrees, 1)
    print(degrees.shape)
    tree_angles = np.expand_dims(tree_angles, 1)
    print(tree_angles.shape)
    out = np.hstack((degrees, lengths, tree_angles))

    np.savetxt(out_filename, out, delimiter=",")
    print(out.shape)


if __name__ == "__main__":
    for i in range(20):
        main(i)
