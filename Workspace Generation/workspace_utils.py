import numpy as np

def eval_poly(coeff, x, y, z):
    """
    Evaluate quadratic polynomial at grid points.
    
    Args:
        coeff: Coefficient array [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9]
        x, y, z: Grid coordinates
    
    Returns:
        Polynomial values at grid points
    """
    return (coeff[0] + coeff[1]*x + coeff[2]*y + coeff[3]*z +
            coeff[4]*x**2 + coeff[5]*y**2 + coeff[6]*z**2 +
            coeff[7]*x*y + coeff[8]*y*z + coeff[9]*z*x)

def create_parameter_grid(alpha_min, alpha_max, beta_min, beta_max, 
                         gamma_min, gamma_max, step):
    """
    Create parameter grid for orientation angles.
    
    Args:
        alpha_min, alpha_max: Alpha angle range
        beta_min, beta_max: Beta angle range  
        gamma_min, gamma_max: Gamma angle range
        step: Step size for grid
    
    Returns:
        List of parameter combinations
    """
    alphas = np.arange(alpha_min, alpha_max + step, step)
    betas = np.arange(beta_min, beta_max + step, step)
    gammas = np.arange(gamma_min, gamma_max + step, step)
    
    # Create all combinations
    param_combinations = []
    for alpha in alphas:
        for beta in betas:
            for gamma in gammas:
                param_combinations.append([alpha, beta, gamma])
    
    return param_combinations

def create_position_grid():
    """
    Create position grid for q1, q2, q3 (matching MATLAB: 0.4:0.2:0.6).
    
    Returns:
        List of position combinations
    """
    q1_values = np.arange(0.4, 0.6 + 0.01, 0.2)
    q2_values = np.arange(0.4, 0.6 + 0.01, 0.2)
    q3_values = np.arange(0.4, 0.6 + 0.01, 0.2)
    
    position_combinations = []
    for q1 in q1_values:
        for q2 in q2_values:
            for q3 in q3_values:
                position_combinations.append([q1, q2, q3])
    
    return position_combinations

def compute_intersection_points(all_points):
    """
    Compute intersection of multiple point sets.
    
    Args:
        all_points: List of point arrays
    
    Returns:
        Intersection points array
    """
    if not all_points:
        return np.empty((0, 3))
    
    intersection = all_points[0]
    for pts in all_points[1:]:
        if len(intersection) == 0 or len(pts) == 0:
            intersection = np.empty((0, 3))
            break
        
        dtype = [('x', float), ('y', float), ('z', float)]
        intersection_view = intersection.view(dtype)
        pts_view = pts.view(dtype)
        intersection = np.intersect1d(intersection_view, pts_view).view(float).reshape(-1, 3)
    
    return intersection 