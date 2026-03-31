# Architecture

LinDelInt is built around a "Compute Mesh" architecture based on **Delaunay Triangulation**.

## Data Flow

1.  **Ingestion:** Base points and their associated properties are provided.
2.  **Triangulation:** A Delaunay mesh is constructed using the `Qhull` library (via SciPy).
3.  **Search:** Query points are mapped to their containing simplex (tetrahedron in 3D, triangle in 2D).
4.  **Interpolation:** 
    - **Inside:** Linear interpolation using barycentric coordinates.
    - **Outside:** Points are projected onto the closest boundary element in a cascading priority: 
        - Face (Triangle) -> Edge -> Vertex.

## Modular Engines

To balance portability and performance, LinDelInt implements four execution engines:
- **Sequential:** Legacy logic (used as reference).
- **Vectorized:** NumPy-based massive array operations (Standard).
- **Parallel:** Numba-compiled kernels with multi-threading (Extreme CPU).
- **GPU:** CuPy-based massively parallel execution (Massive Scale).

The `Interpolator` factory selects the best engine automatically based on the environment.
