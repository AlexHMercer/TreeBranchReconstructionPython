import numpy as np


def sor_filter(cloud, omega=1.5, max_iter=1000, tol=1e-6):
    """
    SOR filter implementation
    """
    # Initialize variables
    n = cloud.shape[0]
    x = np.zeros(n)
    x_new = np.zeros(n)
    residual = np.inf
    iter_count = 0

    # Compute matrix A and vector b
    A = np.zeros((n, n))
    b = np.zeros(n)
    for i in range(n):
        A[i, i] = -2
        b[i] = -2 * cloud[i]

        if i > 0:
            A[i, i-1] = 1
            A[i-1, i] = 1

    # SOR iteration
    while residual > tol and iter_count < max_iter:
        x_new[0] = (1 - omega) * x[0] + omega * (x[1] + b[0]) / -2
        for i in range(1, n-1):
            x_new[i] = (1 - omega) * x[i] + omega * (x_new[i-1] + x[i+1] + b[i]) / -2
        x_new[n-1] = (1 - omega) * x[n-1] + omega * (x[n-2] + b[n-1]) / -2

        residual = np.linalg.norm(x_new - x)
        x[:] = x_new[:]
        iter_count += 1

    return x