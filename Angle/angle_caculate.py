import numpy as np


def calculate(v1, v2):
    cos_value = np.sum(v1*v2) / (np.sqrt(np.sum(v1**2)) * np.sqrt(np.sum(v2**2)))
    print(cos_value)
    print(np.arccos(cos_value) / np.pi * 180)


def main():
    parent = np.array([9.320889, -18.473625, 2.544609])
    child1 = np.array([9.325063, -18.474825, 2.584372])
    child2 = np.array([9.296435, -18.504982, 2.548943])

    v1 = child1 - parent
    v2 = child2 - parent

    calculate(v1, v2)


if __name__ == "__main__":
    main()

