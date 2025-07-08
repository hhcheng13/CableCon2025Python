# Cable Robot Workspace Analysis - Modular Structure

This project has been refactored into a modular structure for better organization and maintainability. The original large `run_analysis` function has been separated into several focused modules.

## Project Structure

```
├── main_workspace_gui.py          # Main GUI application (simplified)
├── workspace_analyzer.py          # Core analysis logic
├── workspace_visualizer.py        # Plotting and visualization
├── workspace_data_manager.py      # Data saving/loading
├── workspace_utils.py             # Utility functions
├── example_usage.py               # Example usage script
├── README_MODULAR.md              # This documentation
└── [existing files]               # Original supporting files
```

## Module Descriptions

### 1. `workspace_utils.py`
**Purpose**: Common utility functions used across the workspace analysis.

**Key Functions**:
- `eval_poly()`: Evaluate quadratic polynomial at grid points
- `create_parameter_grid()`: Create parameter grid for orientation angles
- `create_position_grid()`: Create position grid for q1, q2, q3
- `compute_intersection_points()`: Compute intersection of multiple point sets

### 2. `workspace_analyzer.py`
**Purpose**: Core workspace analysis logic.

**Key Classes**:
- `WorkspaceAnalyzer`: Main analysis class

**Key Methods**:
- `initialize_robot_config()`: Initialize cable robot configuration
- `create_spatial_grid()`: Create spatial grid around reference point
- `compute_valid_region()`: Compute valid region based on polynomial coefficients
- `compute_valid_region_optimized()`: Optimized version that processes all coefficients at once
- `analyze_single_cable()`: Analyze workspace for a single cable (original algorithm)
- `analyze_single_cable_optimized()`: Analyze workspace for a single cable (optimized algorithm)
- `run_full_analysis()`: Run full workspace analysis for all cables (with optimization option)

### 3. `workspace_visualizer.py`
**Purpose**: Plotting and visualization of workspace results.

**Key Classes**:
- `WorkspaceVisualizer`: Visualization class

**Key Methods**:
- `plot_workspace_3d()`: Create 3D visualization using convex hulls
- `plot_comparison()`: Compare Python and MATLAB results
- `plot_scatter_3d()`: Create 3D scatter plot
- `show_plot()`: Display the current plot

### 4. `workspace_data_manager.py`
**Purpose**: Data saving, loading, and management.

**Key Classes**:
- `WorkspaceDataManager`: Data management class

**Key Methods**:
- `save_workspace_data()`: Save workspace intersection points
- `load_workspace_data()`: Load workspace intersection points
- `load_matlab_data()`: Load MATLAB workspace data
- `get_file_info()`: Get information about saved files
- `list_saved_files()`: List all saved workspace files

### 5. `main_workspace_gui.py` (Updated)
**Purpose**: Simplified GUI that uses the modular structure.

**Key Changes**:
- Removed the large `run_analysis()` function
- Now uses the modular classes for analysis, visualization, and data management
- Much cleaner and more maintainable code

## Usage Examples

### Basic Usage with GUI
```python
# Run the GUI application
python main_workspace_gui.py
```

### Programmatic Usage
```python
from workspace_analyzer import WorkspaceAnalyzer
from workspace_visualizer import WorkspaceVisualizer
from workspace_data_manager import WorkspaceDataManager

# Initialize modules
analyzer = WorkspaceAnalyzer()
visualizer = WorkspaceVisualizer()
data_manager = WorkspaceDataManager()

# Run analysis
intersection_points_sets, total_time = analyzer.run_full_analysis(
    alpha_min=0, alpha_max=0,
    beta_min=0, beta_max=0,
    gamma_min=0, gamma_max=0,
    step=0.02
)

# Save results
data_manager.save_workspace_data(intersection_points_sets)

# Visualize results
visualizer.plot_workspace_3d(intersection_points_sets)
visualizer.show_plot()
```

### Example Script
Run the provided example script to see the modular structure in action:
```bash
python example_usage.py
```

## Benefits of the Modular Structure

1. **Separation of Concerns**: Each module has a specific responsibility
2. **Reusability**: Modules can be used independently
3. **Maintainability**: Easier to modify and debug individual components
4. **Testability**: Each module can be tested separately
5. **Readability**: Code is more organized and easier to understand
6. **Extensibility**: Easy to add new features or modify existing ones

## Migration from Original Code

The original `run_analysis()` function has been broken down as follows:

| Original Function Part | New Module | New Method/Class |
|----------------------|------------|------------------|
| Parameter extraction | `main_workspace_gui.py` | `run_analysis()` |
| Grid creation | `workspace_analyzer.py` | `create_spatial_grid()` |
| Polynomial evaluation | `workspace_utils.py` | `eval_poly()` |
| Valid region computation | `workspace_analyzer.py` | `compute_valid_region()` |
| Intersection calculation | `workspace_utils.py` | `compute_intersection_points()` |
| Data saving | `workspace_data_manager.py` | `save_workspace_data()` |
| Visualization | `workspace_visualizer.py` | `plot_workspace_3d()` |

## Dependencies

The modular structure uses the same dependencies as the original code:
- `numpy`
- `matplotlib`
- `scipy`
- `tkinter` (for GUI)

## File Formats

- **Python workspace data**: `.npz` files (NumPy compressed format)
- **MATLAB comparison**: `.mat` files (MATLAB format)

## Performance Optimization

The modular structure includes a significant performance optimization:

### Algorithm Optimization
- **Original Algorithm**: Computes valid region for each parameter combination in nested loops
- **Optimized Algorithm**: Pre-computes all coefficients, then computes valid region once for all combinations

### Performance Benefits
- **Complexity**: Reduced from O(n × m × grid_size) to O(n × m + grid_size)
- **Speedup**: Significant performance improvement, especially for fine grid resolutions
- **Memory**: More efficient memory usage by avoiding redundant computations

### Usage
- **Default**: The GUI and example scripts use the optimized algorithm by default
- **Control**: Set `use_optimized=False` in `run_full_analysis()` to use the original algorithm

### Verification
The optimization maintains identical results while providing substantial performance improvements. 