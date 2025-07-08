import numpy as np
import time
from cable_robot_config import get_cable_robot_config
from compute_h_i_u_coefficients import compute_h_i_u_coefficients
from workspace_utils import eval_poly, create_parameter_grid, create_position_grid, compute_intersection_points

class WorkspaceAnalyzer:
    def __init__(self):
        self.base_points = None
        self.ee_points = None
        self.num_cables = 0
        
    def initialize_robot_config(self):
        """Initialize cable robot configuration."""
        self.base_points, self.ee_points = get_cable_robot_config()
        self.num_cables = self.base_points.shape[1]
        print(f"[DEBUG] Initialized robot with {self.num_cables} cables")
    
    def create_spatial_grid(self, reference_point, step):
        """
        Create spatial grid around a reference point.
        
        Args:
            reference_point: Center point for the grid
            step: Grid step size
            
        Returns:
            xGrid, yGrid, zGrid: 3D grid arrays
        """
        x = np.arange(reference_point[0] - 0.5, reference_point[0] + 0.5 + step, step)
        y = np.arange(reference_point[1] - 0.5, reference_point[1] + 0.5 + step, step)
        z = np.arange(reference_point[2] - 0.5, reference_point[2] + 0.5 + step, step)
        xGrid, yGrid, zGrid = np.meshgrid(x, y, z, indexing='ij')
        return xGrid, yGrid, zGrid
    
    def compute_valid_region_optimized(self, all_coeffs, xGrid, yGrid, zGrid):
        """
        Compute valid region for all coefficient sets at once.
        
        Args:
            all_coeffs: List of coefficient matrices for all parameter combinations
            xGrid, yGrid, zGrid: 3D grid arrays
            
        Returns:
            validRegion: Boolean mask of valid points (intersection of all valid regions)
        """
        if not all_coeffs:
            return np.zeros(xGrid.shape, dtype=bool)
        
        # Initialize valid region as True (all points valid initially)
        validRegion = np.ones(xGrid.shape, dtype=bool)
        
        print(f"[DEBUG] Computing valid region for {len(all_coeffs)} coefficient sets...")
        
        for i, coeffs in enumerate(all_coeffs):
            # Compute valid region for this coefficient set
            coeff_det = coeffs[:, -1]
            polyValues_det = eval_poly(coeff_det, xGrid, yGrid, zGrid)
            current_valid = np.ones(xGrid.shape, dtype=bool)
            
            for j in range(6):
                coeff = coeffs[:, j]
                polyValues = eval_poly(coeff, xGrid, yGrid, zGrid)
                polyValues = np.sign(polyValues_det) * polyValues
                current_valid &= (polyValues < 0)
            
            # Intersection with overall valid region (AND operation)
            validRegion &= current_valid
            
            if (i + 1) % 100 == 0:
                print(f"[DEBUG] Processed {i + 1}/{len(all_coeffs)} coefficient sets")
        
        return validRegion
    
    def compute_valid_region(self, coeffs, xGrid, yGrid, zGrid):
        """
        Compute valid region based on polynomial coefficients.
        
        Args:
            coeffs: Coefficient matrix
            xGrid, yGrid, zGrid: 3D grid arrays
            
        Returns:
            validRegion: Boolean mask of valid points
        """
        coeff_det = coeffs[:, -1]
        polyValues_det = eval_poly(coeff_det, xGrid, yGrid, zGrid)
        validRegion = np.ones(xGrid.shape, dtype=bool)
        
        for i in range(6):
            coeff = coeffs[:, i]
            polyValues = eval_poly(coeff, xGrid, yGrid, zGrid)
            polyValues = np.sign(polyValues_det) * polyValues
            validRegion &= (polyValues < 0)
        
        return validRegion
    
    def extract_valid_points(self, xGrid, yGrid, zGrid, validRegion):
        """
        Extract valid points from grid based on valid region mask.
        
        Args:
            xGrid, yGrid, zGrid: 3D grid arrays
            validRegion: Boolean mask of valid points
            
        Returns:
            points: Array of valid 3D points
        """
        xValid = xGrid[validRegion]
        yValid = yGrid[validRegion]
        zValid = zGrid[validRegion]
        points = np.column_stack((xValid, yValid, zValid))
        return points
    
    def analyze_single_cable_optimized(self, cable_index, alpha_min, alpha_max, beta_min, beta_max,
                                     gamma_min, gamma_max, step):
        """
        Analyze workspace for a single cable (optimized version).
        
        Args:
            cable_index: Index of the cable to analyze
            alpha_min, alpha_max: Alpha angle range
            beta_min, beta_max: Beta angle range
            gamma_min, gamma_max: Gamma angle range
            step: Grid step size
            
        Returns:
            intersection_points: Array of intersection points
            computation_time: Time taken for computation
        """
        print(f"[DEBUG] Processing cable {cable_index+1}/{self.num_cables} (optimized)")
        
        reference_point = self.base_points[:, cable_index]
        xGrid, yGrid, zGrid = self.create_spatial_grid(reference_point, step)
        
        # Start timing
        t_start = time.time()
        
        # Get parameter combinations
        position_combinations = create_position_grid()
        orientation_combinations = create_parameter_grid(
            alpha_min, alpha_max, beta_min, beta_max, gamma_min, gamma_max, step
        )
        
        total_combinations = len(position_combinations) * len(orientation_combinations)
        print(f"[DEBUG] Total parameter combinations: {total_combinations}")
        
        # Pre-compute all coefficients
        print("[DEBUG] Pre-computing all coefficients...")
        t_coeff_start = time.time()
        all_coeffs = []
        q = np.zeros(6)
        
        for i, (q1, q2, q3) in enumerate(position_combinations):
            for alpha, beta, gamma in orientation_combinations:
                q[0] = q1
                q[1] = q2
                q[2] = q3
                q[3] = alpha
                q[4] = beta
                q[5] = gamma
                
                coeffs = compute_h_i_u_coefficients(self.base_points, self.ee_points, q, cable_index)
                all_coeffs.append(coeffs)
                
                if (i * len(orientation_combinations) + len(all_coeffs)) % 100 == 0:
                    print(f"[DEBUG] Computed {len(all_coeffs)}/{total_combinations} coefficient sets")
        
        t_coeff_end = time.time()
        coeff_time = t_coeff_end - t_coeff_start
        print(f"[TIME] Cable {cable_index+1}: coefficient computation time: {coeff_time:.3f}s")
        
        # Compute valid region once for all coefficients
        print("[DEBUG] Computing valid region for all coefficients...")
        t_valid_start = time.time()
        validRegion = self.compute_valid_region_optimized(all_coeffs, xGrid, yGrid, zGrid)
        t_valid_end = time.time()
        valid_time = t_valid_end - t_valid_start
        print(f"[TIME] Cable {cable_index+1}: valid region computation time: {valid_time:.3f}s")
        
        # Extract valid points
        t_extract_start = time.time()
        intersection_points = self.extract_valid_points(xGrid, yGrid, zGrid, validRegion)
        t_extract_end = time.time()
        extract_time = t_extract_end - t_extract_start
        print(f"[TIME] Cable {cable_index+1}: point extraction time: {extract_time:.3f}s")
        
        # End timing
        t_end = time.time()
        computation_time = t_end - t_start
        
        print(f"[DEBUG] Cable {cable_index+1}: {len(intersection_points)} intersection points")
        print(f"[TIME] Cable {cable_index+1}: total calculation time: {computation_time:.3f}s")
        print(f"[TIME] Cable {cable_index+1}: breakdown - coeff: {coeff_time:.3f}s, valid: {valid_time:.3f}s, extract: {extract_time:.3f}s")
        
        return intersection_points, computation_time
    
    def analyze_single_cable(self, cable_index, alpha_min, alpha_max, beta_min, beta_max,
                           gamma_min, gamma_max, step):
        """
        Analyze workspace for a single cable (original version).
        
        Args:
            cable_index: Index of the cable to analyze
            alpha_min, alpha_max: Alpha angle range
            beta_min, beta_max: Beta angle range
            gamma_min, gamma_max: Gamma angle range
            step: Grid step size
            
        Returns:
            intersection_points: Array of intersection points
            computation_time: Time taken for computation
        """
        print(f"[DEBUG] Processing cable {cable_index+1}/{self.num_cables}")
        
        reference_point = self.base_points[:, cable_index]
        xGrid, yGrid, zGrid = self.create_spatial_grid(reference_point, step)
        grid_shape = xGrid.shape
        
        all_points = []
        q = np.zeros(6)
        
        # Start timing
        t_start = time.time()
        
        # Get parameter combinations
        position_combinations = create_position_grid()
        orientation_combinations = create_parameter_grid(
            alpha_min, alpha_max, beta_min, beta_max, gamma_min, gamma_max, step
        )
        
        # Process all combinations
        for q1, q2, q3 in position_combinations:
            for alpha, beta, gamma in orientation_combinations:
                q[0] = q1
                q[1] = q2
                q[2] = q3
                q[3] = alpha
                q[4] = beta
                q[5] = gamma
                
                coeffs = compute_h_i_u_coefficients(self.base_points, self.ee_points, q, cable_index)
                validRegion = self.compute_valid_region(coeffs, xGrid, yGrid, zGrid)
                points = self.extract_valid_points(xGrid, yGrid, zGrid, validRegion)
                all_points.append(points)
        
        # Compute intersection
        intersection_points = compute_intersection_points(all_points)
        
        # End timing
        t_end = time.time()
        computation_time = t_end - t_start
        
        print(f"[DEBUG] Cable {cable_index+1}: {len(intersection_points)} intersection points")
        print(f"[TIME] Cable {cable_index+1}: intersection calculation time: {computation_time:.3f}s")
        
        return intersection_points, computation_time
    
    def run_full_analysis(self, alpha_min, alpha_max, beta_min, beta_max,
                         gamma_min, gamma_max, step, use_optimized=True):
        """
        Run full workspace analysis for all cables.
        
        Args:
            alpha_min, alpha_max: Alpha angle range
            beta_min, beta_max: Beta angle range
            gamma_min, gamma_max: Gamma angle range
            step: Grid step size
            use_optimized: Whether to use the optimized version
            
        Returns:
            intersection_points_sets: List of intersection points for each cable
            total_time: Total computation time
        """
        if self.base_points is None:
            self.initialize_robot_config()
        
        print(f"[DEBUG] Input Ranges: alpha=({alpha_min},{alpha_max}), beta=({beta_min},{beta_max}), gamma=({gamma_min},{gamma_max}), step={step}")
        print(f"[DEBUG] Using {'optimized' if use_optimized else 'original'} algorithm")
        
        intersection_points_sets = [None] * self.num_cables
        total_time = 0
        
        for cable_index in range(self.num_cables):
            if use_optimized:
                intersection_points, cable_time = self.analyze_single_cable_optimized(
                    cable_index, alpha_min, alpha_max, beta_min, beta_max, 
                    gamma_min, gamma_max, step
                )
            else:
                intersection_points, cable_time = self.analyze_single_cable(
                    cable_index, alpha_min, alpha_max, beta_min, beta_max, 
                    gamma_min, gamma_max, step
                )
            intersection_points_sets[cable_index] = intersection_points
            total_time += cable_time
        
        print(f"[TIME] Total analysis time: {total_time:.3f}s")
        return intersection_points_sets, total_time 