import numpy as np

def spatial_model(Base_Points_, End_Effector_Attachment_Points_, q):
    a = Base_Points_
    b = End_Effector_Attachment_Points_
    A, B, G = q[3], q[4], q[5]

    # Rotation matrix R
    R = np.array([
        [np.cos(B)*np.cos(G), -np.cos(B)*np.sin(G), np.sin(B)],
        [np.cos(A)*np.sin(G) + np.sin(A)*np.sin(B)*np.cos(G), np.cos(A)*np.cos(G) - np.sin(A)*np.sin(B)*np.sin(G), -np.sin(A)*np.cos(B)],
        [np.sin(A)*np.sin(G) - np.cos(A)*np.sin(B)*np.cos(G), np.sin(A)*np.cos(G) + np.cos(A)*np.sin(B)*np.sin(G), np.cos(A)*np.cos(B)]
    ])

    # Displacement
    displacement = -q[:3].reshape(3,1) - R @ b + a
    cable_length = np.linalg.norm(displacement, axis=0)
    L_top = (R.T @ displacement) / cable_length
    L_bottom = np.cross(-L_top.T, b.T).T
    L = -np.vstack((L_top, L_bottom))
    # Jacobian is L (6x7)
    return L, cable_length 