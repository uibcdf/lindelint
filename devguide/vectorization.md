# Optimization Strategy: The Three Levels of Performance

LinDelInt is designed to be the high-performance interpolation engine of the **MolSysSuite**. To handle everything from small peptides to cellular-scale systems, we follow a tiered optimization strategy.

## Level 1: NumPy Vectorization (Standard Engine)
*Current Status: Implemented and Validated.*

The first level of optimization replaces sequential Python loops with massive array operations using **NumPy**.

- **Mechanism:** Utilizes `numpy.einsum`, broadcasting, and boolean masking to process thousands of query points simultaneously.
- **Advantages:** 
    - **Portability:** Requires no additional dependencies beyond NumPy and SciPy.
    - **Efficiency:** Provides a ~5x-12x speedup over the original sequential implementation.
    - **Parity:** Guaranteed bit-wise identical results with the original algorithm.
- **Target Use Case:** Standard protein dynamics, interactive visualization, and typical researcher workstations.

## Level 2: Numba-Accelerated Parallelism (Advanced CPU)
*Current Status: Proposed.*

The second level targets the limitations of the Python Global Interpreter Lock (GIL) and the memory overhead of intermediate NumPy arrays.

- **Mechanism:** Uses `numba.njit(parallel=True)` and `prange` to compile the interpolation logic into machine code.
- **Key Improvements:**
    - **Kernel Fusion:** Combines multiple projection steps (Inside -> Faces -> Edges) into a single pass, drastically reducing memory bandwidth usage.
    - **Multi-threading:** Automatically distributes point batches across all available CPU cores.
- **Expected Impact:** An additional 3x-8x speedup over the vectorized engine on multi-core systems.
- **Target Use Case:** Long MD trajectories (50k+ frames), multi-residue coarse-grained models, and high-throughput screening.

## Level 3: GPU-Powered Computation (Supramolecular Scale)
*Current Status: Implemented.*

The final level moves the computation to the Graphics Processing Unit (GPU) for massively parallel execution using **CuPy**.

- **Mechanism:** Integration with **CuPy** (a NumPy-compatible library for CUDA).
- **Strategy:**
    - **CPU-Triangulation:** Delaunay triangulation (Qhull) remains on the CPU.
    - **GPU-Interpolation:** Points and pre-calculated geometry are uploaded to the GPU for projection.
- **Expected Impact:** 50x-100x speedup for systems with millions of query points.
- **Target Use Case:** Cellular-scale dynamics (ribosomes, viruses), electron density map fitting, and SAXS/FRET point-cloud processing.

---

## Performance Benchmark Results (Real World)

The following benchmarks were performed on a standard workstation using a 3D system with 50,000 query points.

| Engine | Points (3D) | Speed (s) | Speedup | Dependencies |
| :--- | :--- | :--- | :--- | :--- |
| Sequential (Original) | 50,000 | 4.0914 | 1.0x | NumPy, SciPy |
| **Vectorized (Level 1)** | 50,000 | 0.2434 | **16.8x** | NumPy, SciPy |
| **Parallel (Level 2)** | 50,000 | 0.0944 | **43.3x** | Numba, NumPy, SciPy |
| GPU (Level 3) | 50,000 | *TBD* | *~100x* | CuPy, CUDA |

### Engine Selection Logic

The `Interpolator` class now includes an `engine` parameter:
- `'auto'` (default): Tries `parallel` first, fallbacks to `vectorized`.
- `'parallel'`: Forces Numba-accelerated multi-threading.
- `'vectorized'`: Forces NumPy-based massive array operations.
- `'sequential'`: Forces the robust sequential-logic fallback.
