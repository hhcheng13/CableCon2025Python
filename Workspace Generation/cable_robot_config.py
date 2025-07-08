import numpy as np

def get_cable_robot_config():
    # Base attachment points (A1 to A7)
    base_points = np.array([
        [0, 1, 1, 0, 0.5, 1, 0],   # x
        [0, 0, 1, 1, 0,   1, 1],   # y
        [1, 1, 1, 1, 0,   0, 0]    # z
    ])
    # End-effector attachment points (B1 to B7)
    ee_points = np.array([
        [-0.15, 0.15, 0.15, -0.15, 0,    0.15, -0.15],  # x
        [-0.1,  -0.1, 0.1,   0.1, -0.1, 0.1,   0.1],   # y
        [0.05, 0.05, 0.05, 0.05, -0.05, -0.05, -0.05]   # z
    ])
    return base_points, ee_points 