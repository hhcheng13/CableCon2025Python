import numpy as np
from numpy.linalg import det

def adjugate(A):
    # Compute the adjugate (classical adjoint) of a 6x6 matrix
    cof = np.zeros_like(A)
    for i in range(6):
        for j in range(6):
            minor = np.delete(np.delete(A, i, axis=0), j, axis=1)
            cof[i, j] = ((-1) ** (i + j)) * det(minor)
    return cof.T

def spatial_model_sampling_rref_last_column_3_variables(Base_Points_, End_Effector_Attachment_Points_, q, debug_info=None):
    a = Base_Points_
    b = End_Effector_Attachment_Points_
    A, B, G = q[3], q[4], q[5]
    # Rotation matrix R
    R = np.array([
        [np.cos(B)*np.cos(G), -np.cos(B)*np.sin(G), np.sin(B)],
        [np.cos(A)*np.sin(G) + np.sin(A)*np.sin(B)*np.cos(G), np.cos(A)*np.cos(G) - np.sin(A)*np.sin(B)*np.sin(G), -np.sin(A)*np.cos(B)],
        [np.sin(A)*np.sin(G) - np.cos(A)*np.sin(B)*np.cos(G), np.sin(A)*np.cos(G) + np.cos(A)*np.sin(B)*np.sin(G), np.cos(A)*np.cos(B)]
    ])
    S = np.array([
        [np.cos(B)*np.cos(G), np.cos(A)*np.sin(G) + np.sin(A)*np.sin(B)*np.cos(G), np.sin(A)*np.sin(G) - np.cos(A)*np.sin(B)*np.cos(G), 0, 0, 0],
        [-np.cos(B)*np.sin(G), np.cos(A)*np.cos(G) - np.sin(A)*np.sin(B)*np.sin(G), np.sin(A)*np.cos(G) + np.cos(A)*np.sin(B)*np.sin(G), 0, 0, 0],
        [np.sin(B), -np.sin(A)*np.cos(B), np.cos(A)*np.cos(B), 0, 0, 0],
        [0, 0, 0, np.cos(B)*np.cos(G), np.sin(G), 0],
        [0, 0, 0, -np.cos(B)*np.sin(G), np.cos(G), 0],
        [0, 0, 0, np.sin(B), 0, 1]
    ])
    displacement = -q[:3].reshape(3,1) - R @ b + a
    cable_length = np.linalg.norm(displacement, axis=0)
    # print(f"[DEBUG] cable_length (shape {cable_length.shape}):\n{np.round(cable_length, 4)}")
    L_top = (R.T @ displacement) / cable_length
    # print(f"[DEBUG] L_top (shape {L_top.shape}):\n{np.round(L_top, 4)}")
    L_bottom = np.cross(-L_top.T, b.T).T
    # print(f"[DEBUG] L_bottom (shape {L_bottom.shape}):\n{np.round(L_bottom, 4)}")
    L = np.vstack((L_top, L_bottom))    
    # print(f"[DEBUG] L (shape {L.shape}):\n{np.round(L, 4)}")
    L_with_norm = -S.T @ L
    # print(f"[DEBUG] L_with_norm (shape {L_with_norm.shape}):\n{np.round(L_with_norm, 4)}")
    L_wo_norm = L_with_norm * cable_length
    # print(f"[DEBUG] L_wo_norm (shape {L_wo_norm.shape}):\n{np.round(L_wo_norm, 4)}")
    # RREF last column: adjugate(L_wo_norm[0:6,0:6]) @ L_wo_norm[:,6]
    A6 = L_wo_norm[:6, :6]
    b6 = L_wo_norm[:, 6]
    adjA6 = adjugate(A6)
    last_column_with_norm_remove_determinant = adjA6 @ b6
    determinant = det(A6)
    # if debug_info is not None:
        
    #     print(f"[DEBUG] last_column_with_norm_remove_determinant (shape {last_column_with_norm_remove_determinant.shape}):\n{np.round(last_column_with_norm_remove_determinant, 9)}")
    #     print(f"[DEBUG] determinant (shape {determinant.shape}):\n{np.round(determinant, 4)}")
    # input("Press Enter to continue to the next pose...")
    return L_with_norm, L_wo_norm, cable_length, last_column_with_norm_remove_determinant, determinant 