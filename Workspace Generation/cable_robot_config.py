import numpy as np

def get_cable_robot_config(num_cables=8):
    """
    Get cable robot configuration for specified number of cables.
    
    Args:
        num_cables: Number of cables (7 or 8)
        
    Returns:
        base_points, ee_points: Arrays of base and end-effector attachment points
    """
    if num_cables == 7:
        return get_7_cable_config()
    elif num_cables == 8:
        return get_8_cable_config()
    else:
        raise ValueError(f"Unsupported number of cables: {num_cables}. Only 7 or 8 cables are supported.")

def get_7_cable_config():
    """Get configuration for 7-cable robot."""
    # Base attachment points (A1 to A7)
    base_points = np.array([
        [0, 1, 1, 0, 0.5, 1, 0],   # x
        [0, 0, 1, 1, 0,   1, 1],   # y
        [1, 1, 1, 1, 0,   0, 0]    # z
    ], dtype=float)
    # End-effector attachment points (B1 to B7)
    ee_points = np.array([
        [-0.15, 0.15, 0.15, -0.15, 0,    0.15, -0.15],  # x
        [-0.1,  -0.1, 0.1,   0.1, -0.1, 0.1,   0.1],   # y
        [0.05, 0.05, 0.05, 0.05, -0.05, -0.05, -0.05]   # z
    ], dtype=float)
    return base_points, ee_points

def get_8_cable_config():
    """Get configuration for 8-cable robot."""
    # Base attachment points (A1 to A8) - adding an 8th cable
    # The 8th cable is positioned to provide additional redundancy
    base_points = np.array([
        [0, 1, 1, 0, 1, 1, 0, 0],   # x
        [0, 0, 1, 1, 0, 1, 1, 0],   # y
        [1, 1, 1, 1, 0, 0, 0, 0]    # z
    ], dtype=float)
    # End-effector attachment points (B1 to B8)
    ee_points = np.array([
        [-0.15, 0.15, 0.15, -0.15, 0.15,    0.15, -0.15, -0.15],  # x
        [-0.1,  -0.1, 0.1,   0.1, -0.1, 0.1,   0.1, -0.1],   # y
        [0.05, 0.05, 0.05, 0.05, -0.05, -0.05, -0.05, -0.05]   # z
    ], dtype=float)
    return base_points, ee_points 