import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from workspace_analyzer import WorkspaceAnalyzer
from workspace_visualizer import WorkspaceVisualizer
from workspace_data_manager import WorkspaceDataManager

class WorkspaceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Cable Robot Workspace Analysis')
        self.create_widgets()
        self.intersection_points_sets = None
        
        # Initialize modules
        self.analyzer = WorkspaceAnalyzer()
        self.visualizer = WorkspaceVisualizer()
        self.data_manager = WorkspaceDataManager()

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
        """Run workspace analysis using the modular structure."""
        try:
            # Extract parameters from GUI
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
        
        # Run analysis using the analyzer module (optimized version)
        self.intersection_points_sets, total_time = self.analyzer.run_full_analysis(
            alpha_min, alpha_max, beta_min, beta_max, gamma_min, gamma_max, step, use_optimized=True
        )
        
        # Visualize results using the visualizer module
        self.visualizer.plot_workspace_3d(self.intersection_points_sets)
        self.visualizer.show_plot()

    def compare_with_matlab(self):
        """Compare Python results with MATLAB results."""
        if self.intersection_points_sets is None:
            messagebox.showerror('Error', 'Please run the analysis first!')
            return
        
        # Let user select the .mat file
        matfile_path = filedialog.askopenfilename(
            title='Select MATLAB Workspace .mat File', 
            filetypes=[('MATLAB files', '*.mat')]
        )
        if not matfile_path:
            return
        
        # Load MATLAB data using the data manager
        matlab_points_list = self.data_manager.load_matlab_data(matfile_path)
        if matlab_points_list is None:
            messagebox.showerror('Error', 'Failed to load MATLAB data!')
            return
        
        # Create comparison plots using the visualizer
        self.visualizer.plot_comparison(self.intersection_points_sets, matlab_points_list)

def main():
    root = tk.Tk()
    app = WorkspaceGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main() 