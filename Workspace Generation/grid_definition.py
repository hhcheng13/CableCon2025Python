import numpy as np

def create_grids(reference_point, grid_range=0.5, step=0.05):
    x = np.arange(reference_point[0] - grid_range, reference_point[0] + grid_range + step, step)
    y = np.arange(reference_point[1] - grid_range, reference_point[1] + grid_range + step, step)
    z = np.arange(reference_point[2] - grid_range, reference_point[2] + grid_range + step, step)
    xGrid, yGrid, zGrid = np.meshgrid(x, y, z, indexing='ij')
    return xGrid, yGrid, zGrid 