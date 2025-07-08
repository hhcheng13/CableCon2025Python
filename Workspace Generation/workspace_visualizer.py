import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from matplotlib.patches import Patch

class WorkspaceVisualizer:
    def __init__(self):
        self.colors = None
        
    def setup_colors(self, num_cables):
        """Setup color scheme for cables."""
        self.colors = plt.cm.jet(np.linspace(0, 1, num_cables))
    
    def plot_workspace_3d(self, intersection_points_sets, title="Workspace Intersection (Convex Hull Surface)"):
        """
        Create 3D visualization of workspace intersection using convex hulls.
        
        Args:
            intersection_points_sets: List of intersection points for each cable
            title: Plot title
        """
        if not intersection_points_sets:
            print("[WARNING] No intersection points to plot")
            return None
        
        num_cables = len(intersection_points_sets)
        if self.colors is None:
            self.setup_colors(num_cables)
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        handles = []
        labels = []
        
        for i, pts in enumerate(intersection_points_sets):
            if pts is not None and len(pts) > 3:
                try:
                    hull = ConvexHull(pts)
                    faces = [pts[simplex] for simplex in hull.simplices]
                    poly = Poly3DCollection(faces, facecolors=[self.colors[i]], alpha=0.2, edgecolor='none')
                    ax.add_collection3d(poly)
                    
                    # Use Patch for legend handle
                    patch = Patch(facecolor=self.colors[i], edgecolor='none', alpha=0.5, label=f'Cable {i+1}')
                    handles.append(patch)
                    labels.append(f'Cable {i+1}')
                except Exception as e:
                    print(f"[PLOT] Cable {i+1}: Convex hull failed, skipping plot - {e}")
        
        # Only add legend if there are handles
        if handles:
            ax.legend(handles, labels, loc='upper left', frameon=False, fontsize=12)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title)
        
        # Gather all points for axis limits
        all_points = np.vstack([pts for pts in intersection_points_sets if pts is not None and len(pts) > 0])
        if all_points.size > 0:
            ax.set_xlim(np.min(all_points[:,0]), np.max(all_points[:,0]))
            ax.set_ylim(np.min(all_points[:,1]), np.max(all_points[:,1]))
            ax.set_zlim(np.min(all_points[:,2]), np.max(all_points[:,2]))
        
        plt.tight_layout()
        return fig, ax
    
    def plot_comparison(self, python_points, matlab_points, num_cables=7):
        """
        Create comparison plots between Python and MATLAB results.
        
        Args:
            python_points: Python intersection points
            matlab_points: MATLAB intersection points
            num_cables: Number of cables to compare
        """
        for i in range(num_cables):
            fig, axes = plt.subplots(1, 2, figsize=(12, 5), subplot_kw={'projection': '3d'})
            
            # MATLAB plot
            axes[0].set_title(f'Cable {i+1} - MATLAB')
            if matlab_points[i].size > 0:
                axes[0].scatter(matlab_points[i][:,0], matlab_points[i][:,1], matlab_points[i][:,2], 
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
    
    def plot_scatter_3d(self, intersection_points_sets, title="Workspace Points (Scatter)"):
        """
        Create 3D scatter plot of workspace points.
        
        Args:
            intersection_points_sets: List of intersection points for each cable
            title: Plot title
        """
        if not intersection_points_sets:
            print("[WARNING] No intersection points to plot")
            return None
        
        num_cables = len(intersection_points_sets)
        if self.colors is None:
            self.setup_colors(num_cables)
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        for i, pts in enumerate(intersection_points_sets):
            if pts is not None and len(pts) > 0:
                ax.scatter(pts[:,0], pts[:,1], pts[:,2], 
                          c=[self.colors[i]], alpha=0.6, s=1, label=f'Cable {i+1}')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title)
        ax.legend()
        
        plt.tight_layout()
        return fig, ax
    
    def show_plot(self):
        """Display the current plot."""
        plt.show() 