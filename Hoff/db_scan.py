from sklearn.cluster import DBSCAN
import numpy as np


def dbscan_filter(cloud, eps=0.05, min_samples=5):
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
    return cloud[core_samples_mask]
