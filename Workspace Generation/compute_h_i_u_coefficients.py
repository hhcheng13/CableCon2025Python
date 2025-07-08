import numpy as np
from sklearn.linear_model import LinearRegression
from spatial_model_sampling_rref_last_column_3_variables import spatial_model_sampling_rref_last_column_3_variables

def compute_h_i_u_coefficients(Base_Points_, End_Effector_Attachment_Points_, q, col, debug_info=None):
    delta = np.array([-0.05, 0, 0.05])
    data = []
    OA_0 = Base_Points_.copy()
    for dx in delta:
        for dy in delta:
            for dz in delta:
                Base_Points_ = OA_0.copy()
                Base_Points_[:, col] += np.array([dx, dy, dz])
                # Use the RREF-based function for constraints
                if debug_info is not None:
                    _, _, _, last_col, determinant = spatial_model_sampling_rref_last_column_3_variables(
                    Base_Points_, End_Effector_Attachment_Points_, q, debug_info)
                else:
                    _, _, _, last_col, determinant = spatial_model_sampling_rref_last_column_3_variables(
                    Base_Points_, End_Effector_Attachment_Points_, q)
                # last_col: shape (6,), determinant: scalar
                constraint_values = np.concatenate((last_col, [determinant]))
                data.append(np.concatenate((Base_Points_[:, col], constraint_values)))
    
    data = np.array(data)
    # print(f"[DEBUG] Data (shape {data.shape}):\n{np.round(data, 9)}")
    # input("Press Enter to continue to the next pose...")
    
    X = data[:, :3]
    Y = data[:, 3:]

    X_poly = np.column_stack([
        np.ones(X.shape[0]),
        X,
        X[:, 0]**2, X[:, 1]**2, X[:, 2]**2,
        X[:, 0]*X[:, 1], X[:, 1]*X[:, 2], X[:, 2]*X[:, 0]
    ])

    coefficients = []
    for i in range(Y.shape[1]):
        reg = LinearRegression(fit_intercept=False)
        reg.fit(X_poly, Y[:, i])
        coefficients.append(reg.coef_)
    coefficients = np.array(coefficients).T  # (10,7)
   
    return coefficients 