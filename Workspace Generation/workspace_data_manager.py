import numpy as np
from scipy.io import loadmat
import os

class WorkspaceDataManager:
    def __init__(self):
        self.default_filename = 'python_workspace_points.npz'
    
    def save_workspace_data(self, intersection_points_sets, filename=None):
        """
        Save workspace intersection points to file.
        
        Args:
            intersection_points_sets: List of intersection points for each cable
            filename: Output filename (optional)
        """
        if filename is None:
            filename = self.default_filename
        
        # Create dictionary for np.savez
        data_dict = {f'cable_{i+1}': arr for i, arr in enumerate(intersection_points_sets)}
        
        try:
            np.savez(filename, **data_dict)
            print(f"[SAVE] Workspace data saved to {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to save workspace data: {e}")
    
    def load_workspace_data(self, filename=None):
        """
        Load workspace intersection points from file.
        
        Args:
            filename: Input filename (optional)
            
        Returns:
            intersection_points_sets: List of intersection points for each cable
        """
        if filename is None:
            filename = self.default_filename
        
        try:
            data = np.load(filename)
            intersection_points_sets = []
            
            # Extract data for each cable
            i = 1
            while f'cable_{i}' in data:
                intersection_points_sets.append(data[f'cable_{i}'])
                i += 1
            
            print(f"[LOAD] Workspace data loaded from {filename}")
            return intersection_points_sets
            
        except Exception as e:
            print(f"[ERROR] Failed to load workspace data: {e}")
            return None
    
    def load_matlab_data(self, matfile_path):
        """
        Load MATLAB workspace data from .mat file.
        
        Args:
            matfile_path: Path to MATLAB .mat file
            
        Returns:
            matlab_points_list: List of MATLAB intersection points for each cable
        """
        try:
            mat = loadmat(matfile_path)
            matlab_points = mat['intersectionPointsSets']
            matlab_points_list = []
            
            for i in range(matlab_points.shape[1]):
                arr = matlab_points[0, i]
                if arr.size == 0:
                    matlab_points_list.append(np.empty((0, 3)))
                else:
                    matlab_points_list.append(np.array(arr))
            
            print(f"[LOAD] MATLAB data loaded from {matfile_path}")
            return matlab_points_list
            
        except Exception as e:
            print(f"[ERROR] Failed to load MATLAB data: {e}")
            return None
    
    def get_file_info(self, filename=None):
        """
        Get information about saved workspace data file.
        
        Args:
            filename: Filename to check (optional)
            
        Returns:
            info_dict: Dictionary with file information
        """
        if filename is None:
            filename = self.default_filename
        
        info = {
            'exists': os.path.exists(filename),
            'filename': filename,
            'size': None,
            'num_cables': 0
        }
        
        if info['exists']:
            try:
                info['size'] = os.path.getsize(filename)
                data = np.load(filename)
                info['num_cables'] = len([k for k in data.keys() if k.startswith('cable_')])
            except Exception as e:
                print(f"[WARNING] Could not read file info: {e}")
        
        return info
    
    def list_saved_files(self, directory='.'):
        """
        List all saved workspace files in directory.
        
        Args:
            directory: Directory to search (default: current directory)
            
        Returns:
            file_list: List of workspace data files
        """
        workspace_files = []
        
        try:
            for filename in os.listdir(directory):
                if filename.endswith('.npz') and 'workspace' in filename.lower():
                    filepath = os.path.join(directory, filename)
                    info = self.get_file_info(filepath)
                    workspace_files.append(info)
        except Exception as e:
            print(f"[ERROR] Could not list files: {e}")
        
        return workspace_files 