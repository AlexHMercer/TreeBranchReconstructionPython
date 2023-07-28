import numpy
from sklearn.cluster import DBSCAN
import numpy as np
from extratSkeleton.Leaf import Leaf


def dbscan_filter(leaves: list, noise: list, eps=0.5, min_samples=6):
    cloud = numpy.empty((0, 3))
    for leaf in leaves:
        cloud = np.vstack((cloud, leaf.position))

    out = list()
    # DBSCAN filter implementation
    # Convert point cloud to numpy array
    # cloud = np.array(cloud)
    # Compute DBSCAN
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(cloud)
    # Get indices of core samples
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    # Get labels for each point
    labels = db.labels_
    # Return filtered point cloud
    for leaf in cloud[core_samples_mask]:
        out.append(Leaf(leaf))

    core_samples_mask[:] = True
    core_samples_mask[db.core_sample_indices_] = False

    for leaf in cloud[core_samples_mask]:
        noise.append(Leaf(leaf))

    return out
