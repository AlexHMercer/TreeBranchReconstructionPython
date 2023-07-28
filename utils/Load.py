from numpy import loadtxt


def load_cloud(original_tree_name: object) -> object:
    try:
        points = loadtxt(original_tree_name, delimiter="\t")[:, :3]
        return points
    except ValueError:
        try:
            points = loadtxt(original_tree_name, delimiter=" ")[:, :3]
            return points
        except ValueError:
            try:
                points = loadtxt(original_tree_name, delimiter=",")[:, :3]
                return points
            except ValueError:
                print("extract tree skeleton: load point cloud data error, please check the file format")
                return None


