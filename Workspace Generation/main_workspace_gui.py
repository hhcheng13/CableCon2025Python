import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from cable_robot_config import get_cable_robot_config
from grid_definition import create_grids
from compute_h_i_u_coefficients import compute_h_i_u_coefficients
from scipy.io import loadmat
from scipy.spatial import ConvexHull
import os
import pickle
import time
from matplotlib.patches import Patch

# Helper: Evaluate quadratic polynomial at grid points
def eval_poly(coeff, x, y, z):
    return (coeff[0] + coeff[1]*x + coeff[2]*y + coeff[3]*z +
            coeff[4]*x**2 + coeff[5]*y**2 + coeff[6]*z**2 +
            coeff[7]*x*y + coeff[8]*y*z + coeff[9]*z*x)

class WorkspaceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Cable Robot Workspace Analysis')
        self.create_widgets()
        self.intersection_points_sets = None

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky='nsew')
        labels = ['x_min', 'x_max', 'y_min', 'y_max', 'z_min', 'z_max', 'alpha_min', 'alpha_max', 'beta_min', 'beta_max', 'gamma_min', 'gamma_max']
        self.entries = {}
        default_vals = ['0.4', '0.6', '0.4', '0.6', '0.4', '0.6', '0', '0', '0', '0', '0', '0']
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky='e')
            entry = ttk.Entry(frame)
            entry.insert(0, default_vals[i])
            entry.grid(row=i, column=1)
            self.entries[label] = entry
        # Add density (step size) entry
        ttk.Label(frame, text='Grid Step Size').grid(row=len(labels), column=0, sticky='e')
        self.density_entry = ttk.Entry(frame)
        self.density_entry.insert(0, '0.02')  # Default to 0.02 to match MATLAB
        self.density_entry.grid(row=len(labels), column=1)
        run_btn = ttk.Button(frame, text='Run Analysis', command=self.run_analysis)
        run_btn.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
        compare_btn = ttk.Button(frame, text='Compare with MATLAB', command=self.compare_with_matlab)
        compare_btn.grid(row=len(labels)+2, column=0, columnspan=2, pady=10)

    def run_analysis(self):
        try:
            x_min = float(self.entries['x_min'].get())
            x_max = float(self.entries['x_max'].get())
            y_min = float(self.entries['y_min'].get())
            y_max = float(self.entries['y_max'].get())
            z_min = float(self.entries['z_min'].get())
            z_max = float(self.entries['z_max'].get())
            alpha_min = float(self.entries['alpha_min'].get())
            alpha_max = float(self.entries['alpha_max'].get())
            beta_min = float(self.entries['beta_min'].get())
            beta_max = float(self.entries['beta_max'].get())
            gamma_min = float(self.entries['gamma_min'].get())
            gamma_max = float(self.entries['gamma_max'].get())
            step = float(self.density_entry.get())
        except ValueError:
            messagebox.showerror('Input Error', 'Please enter valid numbers for all fields.')
            return
        print(f"[DEBUG] Input Ranges: x=({x_min},{x_max}), y=({y_min},{y_max}), z=({z_min},{z_max}), ")
        print(f"        alpha=({alpha_min},{alpha_max}), beta=({beta_min},{beta_max}), gamma=({gamma_min},{gamma_max}), step={step}")
        base_points, ee_points = get_cable_robot_config()
        # Initialize q (will be set in the loop)
        q = np.zeros(6)
        num_cables = base_points.shape[1]
        intersection_points_sets = [None] * num_cables
        for currect_col in range(num_cables):
            print(f"[DEBUG] Processing cable {currect_col+1}/{num_cables}")
            reference_point = base_points[:, currect_col]
            # Use MATLAB-matching grid
            x = np.arange(reference_point[0] - 0.5, reference_point[0] + 0.5 + step, step)
            y = np.arange(reference_point[1] - 0.5, reference_point[1] + 0.5 + step, step)
            z = np.arange(reference_point[2] - 0.5, reference_point[2] + 0.5 + step, step)
            xGrid, yGrid, zGrid = np.meshgrid(x, y, z, indexing='ij')
            grid_shape = xGrid.shape
            all_points = []
            # Start timing intersection calculation
            t_intersection0 = time.time()
            # Loop q1, q2, q3 as in MATLAB: 0.4:0.2:0.6
            for q1 in np.arange(0.4, 0.6+0.01, 0.2):
                for q2 in np.arange(0.4, 0.6+0.01, 0.2):
                    for q3 in np.arange(0.4, 0.6+0.01, 0.2):
                        for alpha in np.arange(alpha_min, alpha_max+step, step):
                            for beta in np.arange(beta_min, beta_max+step, step):
                                for gamma in np.arange(gamma_min, gamma_max+step, step):
                                    q[0] = q1
                                    q[1] = q2
                                    q[2] = q3
                                    q[3] = alpha
                                    q[4] = beta
                                    q[5] = gamma
                                    coeffs = compute_h_i_u_coefficients(base_points, ee_points, q, currect_col)
                                    coeff_det = coeffs[:, -1]
                                    polyValues_det = eval_poly(coeff_det, xGrid, yGrid, zGrid)
                                    validRegion = np.ones(grid_shape, dtype=bool)
                                    for i in range(6):
                                        coeff = coeffs[:, i]
                                        polyValues = eval_poly(coeff, xGrid, yGrid, zGrid)
                                        polyValues = np.sign(polyValues_det) * polyValues
                                        validRegion &= (polyValues < 0)
                                    xValid = xGrid[validRegion]
                                    yValid = yGrid[validRegion]
                                    zValid = zGrid[validRegion]
                                    points = np.column_stack((xValid, yValid, zValid))
                                    all_points.append(points)
            if all_points:
                intersection = all_points[0]
                for pts in all_points[1:]:
                    if len(intersection) == 0 or len(pts) == 0:
                        intersection = np.empty((0,3))
                        break
                    dtype = [('x', float), ('y', float), ('z', float)]
                    intersection_view = intersection.view(dtype)
                    pts_view = pts.view(dtype)
                    intersection = np.intersect1d(intersection_view, pts_view).view(float).reshape(-1,3)
                intersection_points_sets[currect_col] = intersection
                print(f"[DEBUG] Cable {currect_col+1}: {len(intersection)} intersection points")
            else:
                intersection_points_sets[currect_col] = np.empty((0,3))
            # End timing intersection calculation
            t_intersection1 = time.time()
            print(f"[TIME] Cable {currect_col+1}: intersection calculation time: {t_intersection1-t_intersection0:.3f}s")
        self.intersection_points_sets = intersection_points_sets
        # Save using np.savez (fix ValueError for inhomogeneous shapes)
        np.savez('python_workspace_points.npz', **{f'cable_{i+1}': arr for i, arr in enumerate(intersection_points_sets)})
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        colors = plt.cm.jet(np.linspace(0, 1, num_cables))
        handles = []
        labels = []
        for i, pts in enumerate(intersection_points_sets):
            if pts is not None and len(pts) > 3:
                try:
                    hull = ConvexHull(pts)
                    faces = [pts[simplex] for simplex in hull.simplices]
                    poly = Poly3DCollection(faces, facecolors=[colors[i]], alpha=0.2, edgecolor='none')
                    ax.add_collection3d(poly)
                    # Use Patch for legend handle
                    patch = Patch(facecolor=colors[i], edgecolor='none', alpha=0.5, label=f'Cable {i+1}')
                    handles.append(patch)
                    labels.append(f'Cable {i+1}')
                except Exception as e:
                    print(f"[PLOT] Cable {i+1}: Convex hull failed, skipping plot")
        # Only add legend if there are handles
        if handles:
            ax.legend(handles, labels, loc='upper left', frameon=False, fontsize=12)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Workspace Intersection (Convex Hull Surface)')
        # Gather all points for axis limits
        all_points = np.vstack([pts for pts in intersection_points_sets if pts is not None and len(pts) > 0])
        if all_points.size > 0:
            ax.set_xlim(np.min(all_points[:,0]), np.max(all_points[:,0]))
            ax.set_ylim(np.min(all_points[:,1]), np.max(all_points[:,1]))
            ax.set_zlim(np.min(all_points[:,2]), np.max(all_points[:,2]))
        plt.tight_layout()
        plt.show()

    def compare_with_matlab(self):
        if self.intersection_points_sets is None:
            messagebox.showerror('Error', 'Please run the analysis first!')
            return
        # Let user select the .mat file
        matfile_path = filedialog.askopenfilename(title='Select MATLAB Workspace .mat File', filetypes=[('MATLAB files', '*.mat')])
        if not matfile_path:
            return
        mat = loadmat(matfile_path)
        matlab_points = mat['intersectionPointsSets']
        matlab_points_list = []
        for i in range(matlab_points.shape[1]):
            arr = matlab_points[0, i]
            if arr.size == 0:
                matlab_points_list.append(np.empty((0, 3)))
            else:
                matlab_points_list.append(np.array(arr))
        python_points = self.intersection_points_sets
        for i in range(7):
            fig, axes = plt.subplots(1, 2, figsize=(12, 5), subplot_kw={'projection': '3d'})
            # MATLAB plot
            axes[0].set_title(f'Cable {i+1} - MATLAB')
            if matlab_points_list[i].size > 0:
                axes[0].scatter(matlab_points_list[i][:,0], matlab_points_list[i][:,1], matlab_points_list[i][:,2], 
                                c='r', alpha=0.5, s=1)
            axes[0].set_xlabel('X')
            axes[0].set_ylabel('Y')
            axes[0].set_zlabel('Z')
            # Python plot
            axes[1].set_title(f'Cable {i+1} - Python')
            if python_points[i].size > 0:
                axes[1].scatter(python_points[i][:,0], python_points[i][:,1], python_points[i][:,2], 
                                c='b', alpha=0.5, s=1)
            axes[1].set_xlabel('X')
            axes[1].set_ylabel('Y')
            axes[1].set_zlabel('Z')
            plt.tight_layout()
            plt.show()

def main():
    root = tk.Tk()
    app = WorkspaceGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main() 