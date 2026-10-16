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
                    result = spatial_model_sampling_rref_last_column_3_variables(
                        Base_Points_, End_Effector_Attachment_Points_, q, debug_info)
                else:
                    result = spatial_model_sampling_rref_last_column_3_variables(
                        Base_Points_, End_Effector_Attachment_Points_, q)
                # For 7 cables: result is a tuple; for 8 cables: result is a list of tuples
                if isinstance(result, list):
                    # 8-cable case: collect data for each combination
                    for res in result:
                        last_col, determinant = res[3], res[4]
                        constraint_values = np.concatenate((last_col, [determinant]))
                        data.append(np.concatenate((Base_Points_[:, col], constraint_values)))
                else:
                    # 7-cable case
                    last_col, determinant = result[3], result[4]
                    constraint_values = np.concatenate((last_col, [determinant]))
                    data.append(np.concatenate((Base_Points_[:, col], constraint_values)))
    data = np.array(data)
    X = data[:, :3]
    Y = data[:, 3:]
    X_poly = np.column_stack([
        np.ones(X.shape[0]),
        X
    ])
    coefficients = []
    for i in range(Y.shape[1]):
        reg = LinearRegression(fit_intercept=False)
        reg.fit(X_poly, Y[:, i])
        coefficients.append(reg.coef_)
    coefficients = np.array(coefficients).T  # (4,7)
    print(f"Coefficients shape: {coefficients.shape}")
    print(f"Coefficients (rounded to 6 decimal places, transposed):")
    print(np.round(coefficients.T, 6))
    return coefficients 