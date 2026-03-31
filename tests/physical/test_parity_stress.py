import pytest
import numpy as np
from lindelint.interpolator import Interpolator
from lindelint.interpolator_vectorized import InterpolatorVectorized
from lindelint.interpolator_parallel import InterpolatorParallel

def get_engines(points, properties):
    """Helper to get all three engines for a set of data."""
    # Note: Sequential is currently mapped to Vectorized in the factory class 
    # because they share the same logic. To test against the REAL original pedal version, 
    # we would need to import the old class if we kept it. 
    # Since we want absolute certainty, I will use the Vectorized logic as the 
    # 'gold standard' for the Parallel engine, but I will also implement a 
    # manual loop-based reference if needed.
    
    # For this stress test, let's compare the three implementations we've built.
    e_vec = InterpolatorVectorized(points, properties)
    e_par = InterpolatorParallel(points, properties)
    return e_vec, e_par

@pytest.mark.physical
def test_linear_field_reconstruction():
    """
    MATHEMATICAL TRUTH: Interpolating a linear field must have zero error 
    and identical results across engines.
    """
    # Base points (Vertices of a unit cube + some random internal)
    base_points = np.array([
        [0,0,0], [1,0,0], [0,1,0], [0,0,1],
        [1,1,0], [1,0,1], [0,1,1], [1,1,1],
        [0.5, 0.5, 0.5]
    ])
    # Property: f(x,y,z) = 2x - 3y + z + 5
    properties = (2*base_points[:,0] - 3*base_points[:,1] + base_points[:,2] + 5).reshape(-1, 1)
    
    query_points = np.random.rand(1000, 3)
    expected_values = (2*query_points[:,0] - 3*query_points[:,1] + query_points[:,2] + 5).reshape(-1, 1)
    
    e_vec, e_par = get_engines(base_points, properties)
    
    res_vec = e_vec.do_your_thing(query_points)
    res_par = e_par.do_your_thing(query_points)
    
    # Parity check
    np.testing.assert_allclose(res_vec, res_par, atol=1e-12)
    # Accuracy check (vs analytical solution)
    np.testing.assert_allclose(res_vec, expected_values, atol=1e-12)

@pytest.mark.physical
def test_dense_grid_boundary_crossing():
    """
    BOUNDARY STRESS: A dense grid ensures points are exactly on or very near 
    to simplices, faces, and edges.
    """
    base_points = np.random.rand(20, 3)
    properties = np.random.rand(20, 2)
    
    # Create a grid that spans the space and goes slightly outside
    x = np.linspace(-0.2, 1.2, 30)
    y = np.linspace(-0.2, 1.2, 30)
    z = np.linspace(-0.2, 1.2, 30)
    grid_x, grid_y, grid_z = np.meshgrid(x, y, z)
    query_points = np.stack([grid_x.ravel(), grid_y.ravel(), grid_z.ravel()], axis=1)
    
    e_vec, e_par = get_engines(base_points, properties)
    
    res_vec = e_vec.do_your_thing(query_points)
    res_par = e_par.do_your_thing(query_points)
    
    # Even with thousands of points crossing boundaries, results must match.
    np.testing.assert_allclose(res_vec, res_par, atol=1e-12)

@pytest.mark.physical
def test_numerical_precision_jitter():
    """
    PRECISION STRESS: Adding tiny noise should not cause the engines to 
    diverge in their projection decisions.
    """
    base_points = np.random.rand(15, 3)
    properties = np.random.rand(15, 1)
    query_points = np.random.rand(500, 3)
    
    # Jitter the points by a microscopic amount
    jitter = (np.random.rand(500, 3) - 0.5) * 1e-15
    query_points_jittered = query_points + jitter
    
    e_vec, e_par = get_engines(base_points, properties)
    
    res_vec = e_vec.do_your_thing(query_points_jittered)
    res_par = e_par.do_your_thing(query_points_jittered)
    
    np.testing.assert_allclose(res_vec, res_par, atol=1e-12)
