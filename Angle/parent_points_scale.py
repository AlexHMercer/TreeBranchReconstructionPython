import numpy as np


def main(index):
    segment_length = 2
    scales = [2, 2]
    departments = [0, 0.3, 1]

    filename = "five_years_parent_position/" + str(index) + "_position.csv"
    out_filename = "five_years_parent_position/" + str(index) + "_scale_position.csv"

    data = np.loadtxt(filename, delimiter=",")
    degrees = data[:, 0]
    lengths = data[:, 1]
    max_length = max(lengths)

    segments = list()
    for department in departments:
        segments.append(max_length * department)

    expands = list()
    expand_length = 0
    for index in range(len(scales)):
        scale = scales[index]
        expands.append(expand_length)
        expand_length += scale * (segments[index+1] - segments[index])

    tmp = lengths.copy()
    # 分成四段
    for i in range(segment_length):
        for index in range(len(tmp)):
            length = tmp[index]
            if segments[i] < length < segments[i+1]:
                lengths[index] = length * scales[i] + expands[i]

    lengths = np.expand_dims(lengths, 1)
    print(lengths.shape)
    degrees = np.expand_dims(degrees, 1)
    print(degrees.shape)
    out = np.hstack((degrees, lengths))
    np.savetxt(out_filename, out, delimiter=",")
    print(out.shape)


if __name__ == "__main__":
    for i in range(7):
        main(i)
