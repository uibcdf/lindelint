import pytest
import numpy as np
import time
from lindelint.interpolator import Interpolator
from lindelint.interpolator_vectorized import InterpolatorVectorized
from lindelint.interpolator_parallel import InterpolatorParallel

@pytest.mark.smoke
def test_compare_engines_3d():
    # 1. Setup random data (Larger set to see the effect of parallelism)
    n_points_base = 50
    n_points_query = 50000 # Increased to 50k
    dim = 3
    dim_prop = 3
    
    points_base = np.random.rand(n_points_base, dim)
    properties_base = np.random.rand(n_points_base, dim_prop)
    points_query = np.random.rand(n_points_query, dim)
    
    # 2. Original Engine
    t0 = time.time()
    interp_orig = Interpolator(points_base, properties_base)
    res_orig = interp_orig.do_your_thing(points_query)
    t_orig = time.time() - t0
    
    # 3. Vectorized Engine
    t0 = time.time()
    interp_vec = InterpolatorVectorized(points_base, properties_base)
    res_vec = interp_vec.do_your_thing(points_query)
    t_vec = time.time() - t0
    
    # 4. Parallel Engine (Numba)
    # Warmup for JIT
    interp_par = InterpolatorParallel(points_base, properties_base)
    interp_par.do_your_thing(points_query[:100])
    
    t0 = time.time()
    res_par = interp_par.do_your_thing(points_query)
    t_par = time.time() - t0
    
    # 5. Assert results are close
    np.testing.assert_allclose(res_orig, res_vec, atol=1e-10)
    np.testing.assert_allclose(res_orig, res_par, atol=1e-10)
    
    print(f"\n[3D] Points: {n_points_query}")
    print(f"Original:   {t_orig:.4f}s | 1.0x")
    print(f"Vectorized: {t_vec:.4f}s | {t_orig/t_vec:.1f}x")
    print(f"Parallel:   {t_par:.4f}s | {t_orig/t_par:.1f}x (Speedup over Vector: {t_vec/t_par:.1f}x)")
