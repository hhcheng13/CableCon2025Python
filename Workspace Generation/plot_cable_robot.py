import numpy as np
import matplotlib.pyplot as plt
from cable_robot_config import get_cable_robot_config

def rotation_matrix_from_euler(alpha, beta, gamma):
    # ZYX Euler angles
    Rz = np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma),  np.cos(gamma), 0],
        [0, 0, 1]
    ])
    Ry = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha),  np.cos(alpha)]
    ])
    return Rz @ Ry @ Rx

def plot_cable_robot_pose(q):
    base_points, ee_points = get_cable_robot_config()
    # Extract translation and orientation
    pos = q[:3].reshape(3, 1)
    alpha, beta, gamma = q[3], q[4], q[5]
    R = rotation_matrix_from_euler(alpha, beta, gamma)
    # Transform EE points
    ee_points_transformed = R @ ee_points + pos
    # Plot base points
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(base_points[0, :], base_points[1, :], base_points[2, :], c='k', s=60, label='Base Points')
    # Plot transformed EE points
    ax.scatter(ee_points_transformed[0, :], ee_points_transformed[1, :], ee_points_transformed[2, :],
               c='c', s=60, label='EE Points (at pose)')
    # Draw cables and label
    for i in range(base_points.shape[1]):
        ax.plot([base_points[0, i], ee_points_transformed[0, i]],
                [base_points[1, i], ee_points_transformed[1, i]],
                [base_points[2, i], ee_points_transformed[2, i]],
                'b-', lw=2)
        # Label cable number at the midpoint
        mid = (np.array([base_points[:, i], ee_points_transformed[:, i]]).mean(axis=0))
        ax.text(mid[0], mid[1], mid[2], f'{i+1}', color='red', fontsize=12, weight='bold')
    # Plot the end-effector centroid
    ee_centroid = np.mean(ee_points_transformed, axis=1)
    ax.scatter([ee_centroid[0]], [ee_centroid[1]], [ee_centroid[2]], c='m', s=100, marker='*', label='EE Centroid')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Cable Robot at Given Pose')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    q = np.array([0.6, 0.6, 0.6, 0.02, 0, 0])
    plot_cable_robot_pose(q) 