#!/usr/bin/env python3
"""
Test script for 8-cable cable robot system.
This script tests the spatial model function with 8 cables to ensure it works correctly.
"""

import numpy as np
from cable_robot_config import get_cable_robot_config
from spatial_model_sampling_rref_last_column_3_variables import spatial_model_sampling_rref_last_column_3_variables

def test_7_cable_system():
    """Test the 7-cable system (original functionality)."""
    print("=" * 50)
    print("Testing 7-cable system...")
    print("=" * 50)
    
    # Get 7-cable configuration
    base_points, ee_points = get_cable_robot_config(7)
    print(f"Base points shape: {base_points.shape}")
    print(f"End-effector points shape: {ee_points.shape}")
    
    # Test pose
    q = np.array([0.5, 0.5, 0.5, 0.0, 0.0, 0.0])  # [x, y, z, alpha, beta, gamma]
    
    try:
        # Test spatial model
        L_with_norm, L_wo_norm, cable_length, last_column, determinant = spatial_model_sampling_rref_last_column_3_variables(
            base_points, ee_points, q, debug_info=True
        )
        
        print(f"✓ 7-cable system works correctly")
        print(f"  L_with_norm shape: {L_with_norm.shape}")
        print(f"  L_wo_norm shape: {L_wo_norm.shape}")
        print(f"  Cable length shape: {cable_length.shape}")
        print(f"  Last column shape: {last_column.shape}")
        print(f"  Determinant: {determinant}")
        
    except Exception as e:
        print(f"✗ 7-cable system failed: {e}")
        return False
    
    return True

def test_8_cable_system():
    """Test the 8-cable system (new functionality)."""
    print("\n" + "=" * 50)
    print("Testing 8-cable system...")
    print("=" * 50)
    
    # Get 8-cable configuration
    base_points, ee_points = get_cable_robot_config(8)
    print(f"Base points shape: {base_points.shape}")
    print(f"End-effector points shape: {ee_points.shape}")
    
    # Test pose
    q = np.array([0.5, 0.5, 0.5, 0.0, 0.0, 0.0])  # [x, y, z, alpha, beta, gamma]
    
    try:
        # Test spatial model
        L_with_norm, L_wo_norm, cable_length, last_column, determinant = spatial_model_sampling_rref_last_column_3_variables(
            base_points, ee_points, q, debug_info=True
        )
        
        print(f"✓ 8-cable system works correctly")
        print(f"  L_with_norm shape: {L_with_norm.shape}")
        print(f"  L_wo_norm shape: {L_wo_norm.shape}")
        print(f"  Cable length shape: {cable_length.shape}")
        print(f"  Last column shape: {last_column.shape}")
        print(f"  Determinant: {determinant}")
        
    except Exception as e:
        print(f"✗ 8-cable system failed: {e}")
        return False
    
    return True

def test_invalid_cable_count():
    """Test that invalid cable counts are properly handled."""
    print("\n" + "=" * 50)
    print("Testing invalid cable count handling...")
    print("=" * 50)
    
    try:
        # Try to get configuration for 6 cables (should fail)
        base_points, ee_points = get_cable_robot_config(6)
        print("✗ Should have failed for 6 cables")
        return False
    except ValueError as e:
        print(f"✓ Correctly rejected 6 cables: {e}")
    
    try:
        # Try to get configuration for 9 cables (should fail)
        base_points, ee_points = get_cable_robot_config(9)
        print("✗ Should have failed for 9 cables")
        return False
    except ValueError as e:
        print(f"✓ Correctly rejected 9 cables: {e}")
    
    return True

def main():
    """Run all tests."""
    print("Testing Cable Robot System with 7 and 8 Cables")
    print("=" * 60)
    
    # Test 7-cable system
    test1_passed = test_7_cable_system()
    
    # Test 8-cable system
    test2_passed = test_8_cable_system()
    
    # Test error handling
    test3_passed = test_invalid_cable_count()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"7-cable system: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"8-cable system: {'✓ PASSED' if test2_passed else '✗ FAILED'}")
    print(f"Error handling: {'✓ PASSED' if test3_passed else '✗ FAILED'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 All tests passed! The 8-cable system is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main() 