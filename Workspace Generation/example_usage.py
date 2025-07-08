#!/usr/bin/env python3
"""
Example usage of the modular workspace analysis system.

This script demonstrates how to use the separated modules for cable robot workspace analysis.
"""

import numpy as np
from workspace_analyzer import WorkspaceAnalyzer
from workspace_visualizer import WorkspaceVisualizer
from workspace_data_manager import WorkspaceDataManager

def example_basic_analysis():
    """Example of basic workspace analysis."""
    print("=== Basic Workspace Analysis Example ===")
    
    # Initialize modules
    analyzer = WorkspaceAnalyzer()
    visualizer = WorkspaceVisualizer()
    data_manager = WorkspaceDataManager()
    
    # Define analysis parameters
    alpha_min, alpha_max = 0, 0
    beta_min, beta_max = 0, 0
    gamma_min, gamma_max = 0, 0
    step = 0.02
    
    print(f"Analysis parameters:")
    print(f"  Alpha range: [{alpha_min}, {alpha_max}]")
    print(f"  Beta range: [{beta_min}, {beta_max}]")
    print(f"  Gamma range: [{gamma_min}, {gamma_max}]")
    print(f"  Step size: {step}")
    
    # Run analysis
    print("\nRunning analysis...")
    intersection_points_sets, total_time = analyzer.run_full_analysis(
        alpha_min, alpha_max, beta_min, beta_max, gamma_min, gamma_max, step
    )
    
    print(f"\nAnalysis completed in {total_time:.3f} seconds")
    
    # Save results
    data_manager.save_workspace_data(intersection_points_sets, "example_workspace.npz")
    
    # Visualize results
    print("\nCreating visualization...")
    visualizer.plot_workspace_3d(intersection_points_sets, "Example Workspace Analysis")
    visualizer.show_plot()
    
    return intersection_points_sets

def example_load_and_visualize():
    """Example of loading saved data and visualizing."""
    print("\n=== Load and Visualize Example ===")
    
    visualizer = WorkspaceVisualizer()
    data_manager = WorkspaceDataManager()
    
    # Check if we have saved data
    info = data_manager.get_file_info("example_workspace.npz")
    if info['exists']:
        print(f"Loading saved workspace data from {info['filename']}")
        intersection_points_sets = data_manager.load_workspace_data("example_workspace.npz")
        
        if intersection_points_sets:
            print("Creating scatter plot visualization...")
            visualizer.plot_scatter_3d(intersection_points_sets, "Loaded Workspace Data (Scatter)")
            visualizer.show_plot()
    else:
        print("No saved workspace data found. Run basic analysis first.")

def example_parameter_variation():
    """Example of analyzing with different parameters."""
    print("\n=== Parameter Variation Example ===")
    
    analyzer = WorkspaceAnalyzer()
    visualizer = WorkspaceVisualizer()
    
    # Test different step sizes
    step_sizes = [0.05, 0.02, 0.01]
    
    for step in step_sizes:
        print(f"\nAnalyzing with step size: {step}")
        
        intersection_points_sets, total_time = analyzer.run_full_analysis(
            0, 0, 0, 0, 0, 0, step
        )
        
        print(f"  Completed in {total_time:.3f} seconds")
        print(f"  Total points: {sum(len(pts) if pts is not None else 0 for pts in intersection_points_sets)}")
        
        # Save with step size in filename
        data_manager = WorkspaceDataManager()
        data_manager.save_workspace_data(intersection_points_sets, f"workspace_step_{step}.npz")

def main():
    """Main example function."""
    print("Cable Robot Workspace Analysis - Modular Example")
    print("=" * 50)
    
    try:
        # Run basic analysis
        intersection_points_sets = example_basic_analysis()
        
        # Load and visualize saved data
        example_load_and_visualize()
        
        # Parameter variation example (commented out to avoid long execution)
        # example_parameter_variation()
        
        print("\nExample completed successfully!")
        
    except Exception as e:
        print(f"Error in example: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 