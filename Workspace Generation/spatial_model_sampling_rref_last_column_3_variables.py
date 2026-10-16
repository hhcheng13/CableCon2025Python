import numpy as np
from numpy.linalg import det
from itertools import combinations

def adjugate(A):
    # Compute the adjugate (classical adjoint) of a 6x6 matrix
    cof = np.zeros_like(A)
    for i in range(6):
        for j in range(6):
            minor = np.delete(np.delete(A, i, axis=0), j, axis=1)
            cof[i, j] = ((-1) ** (i + j)) * det(minor)
    return cof.T

def spatial_model_sampling_rref_last_column_3_variables(Base_Points_, End_Effector_Attachment_Points_, q, debug_info=None):
    """
    Compute spatial model for cable robot with support for 7 or 8 cables.
    
    For 7 cables: Works as before (7x6 Jacobian)
    For 8 cables: Generates combinations of 7 cables and computes for each combination
    """
    a = Base_Points_
    b = End_Effector_Attachment_Points_
    num_cables = a.shape[1]
    
    if num_cables == 7:
        # Original 7-cable case
        return _compute_spatial_model_7_cables(a, b, q, debug_info)
    elif num_cables == 8:
        # New 8-cable case with combinations
        return _compute_spatial_model_8_cables(a, b, q, debug_info)
    else:
        raise ValueError(f"Unsupported number of cables: {num_cables}. Only 7 or 8 cables are supported.")

def _compute_spatial_model_7_cables(Base_Points_, End_Effector_Attachment_Points_, q, debug_info=None):
    """Original implementation for 7 cables."""
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
    L_top = (R.T @ displacement) / cable_length
    L_bottom = np.cross(-L_top.T, b.T).T
    L = np.vstack((L_top, L_bottom))    
    L_with_norm = -S.T @ L
    L_wo_norm = L_with_norm * cable_length
    A6 = L_wo_norm[:6, :6]
    b6 = L_wo_norm[:, 6]
    adjA6 = adjugate(A6)
    last_column_with_norm_remove_determinant = adjA6 @ b6
    determinant = det(A6)
    return L_with_norm, L_wo_norm, cable_length, last_column_with_norm_remove_determinant, determinant

def _compute_spatial_model_8_cables(Base_Points_, End_Effector_Attachment_Points_, q, debug_info=None):
    """
    Compute spatial model for 8 cables by generating combinations of 7 cables.
    
    Returns:
        List of results for all 7-cable combinations
    """
    a = Base_Points_
    b = End_Effector_Attachment_Points_
    A, B, G = q[3], q[4], q[5]
    
    # Generate all combinations of 7 cables from 8 cables
    cable_combinations = list(combinations(range(8), 7))
    num_combinations = len(cable_combinations)
    
    if debug_info is not None:
        print(f"[DEBUG] Processing {num_combinations} combinations of 7 cables from 8 cables")
    
    # Store results for each combination
    results = []
    
    for i, cable_combo in enumerate(cable_combinations):
        if debug_info is not None:
            print(f"[DEBUG] Processing combination {i+1}/{num_combinations}: cables {[j+1 for j in cable_combo]}")
        
        # Extract 7 cables for this combination
        a_7 = a[:, list(cable_combo)]
        b_7 = b[:, list(cable_combo)]
        
        # Compute spatial model for this 7-cable combination
        result = _compute_spatial_model_7_cables(a_7, b_7, q, debug_info)
        results.append(result)
    
    return results 