# Future Plans: The Next Frontiers of Interpolation

LinDelInt aims to evolve from a high-performance utility into a mathematically sophisticated engine capable of handling the most demanding challenges in computational biophysics and machine learning.

## 1. Periodic Boundary Conditions (PBC) Support

Currently, LinDelInt operates in an infinite Euclidean space. However, most molecular dynamics simulations occur within periodic boxes.

- **Mechanism:** Implement the **Minimum Image Convention (MIC)** within the triangulation and search logic.
- **Application:** Seamlessly interpolate trajectories where atoms cross the simulation box boundaries.
- **Potential Advantages:** Eliminates "tearing" artifacts at the edges of the box, making LinDelInt the first simplicial interpolator natively designed for periodic molecular systems.

## 2. Natural Neighbor Interpolation (Sibson's Method)

Linear interpolation is $C^0$ continuous, meaning values are continuous but gradients (slopes) are not. This creates sharp "kinks" at the boundaries between simplices.

- **Mechanism:** Implement **Natural Neighbor Interpolation**, which uses the volume ratios of Voronoi cells instead of barycentric coordinates.
- **Application:** High-fidelity mapping of force fields and electrostatic potentials where smoothness is critical for physical accuracy.
- **Potential Advantages:** Achieves **$C^1$ continuity (smoothness)**. This provides "cinematic" quality in animations and enables the calculation of reliable gradients (forces) across the entire domain.

## 3. Differentiable Interpolation (AI-Ready Backend)

To power next-generation protein design and machine learning, the interpolation process must be "transparent" to gradients.

- **Mechanism:** Port the vectorized interpolation logic to **JAX** or **PyTorch**.
- **Application:** Use LinDelInt as a layer within a Deep Learning model. For example, to optimize coarse-grained node positions based on full-atom target properties.
- **Potential Advantages:** Enables **Backpropagation through the mesh**. Developers can perform sensitivity analysis (e.g., "how does a shift in the Alpha-Carbons affect the position of the ligand?") and train neural networks that incorporate geometric constraints.

## 4. Memory Chunking and Lazy Geometry

As we scale to cellular systems (millions of atoms), storing the pre-calculated geometry of every face and edge becomes a memory bottleneck.

- **Mechanism:** Implement **Block-based processing (Chunking)** and **On-the-fly Geometry calculation**.
- **Application:** Analysis of massive supramolecular complexes (ribosomes, viral capsids) or high-resolution volumetric maps.
- **Potential Advantages:** Drastically reduces the RAM footprint. This allows researchers to perform extreme-scale interpolations on standard consumer hardware by processing points in manageable batches.

---

## Technical Integration Roadmap

1.  **`pbc=True` option:** Integration with MolSysMT box definitions.
2.  **`engine='jax'`**: Experimental differentiable backend.
3.  **`smooth=True`**: Toggle between Linear and Natural Neighbor interpolation.
4.  **`chunk_size` parameter**: Automatic memory management for large-scale query sets.
