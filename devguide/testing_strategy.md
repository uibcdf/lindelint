# Testing Strategy

LinDelInt follows a Tiered testing protocol to ensure mathematical accuracy and engine performance.

## Tier 1: Smoke Tests (Unit)
- **Purpose:** Ensure the library imports and basic interpolation works.
- **Scope:** 
  - Initialization with 2D and 3D data.
  - **Parity Check:** Verification that Vectorized and Parallel engines yield the same results as the Sequential engine.

## Tier 2: Mathematical Validation (Functional)
- **Purpose:** Verify that the results are mathematically sound.
- **Scope:**
  - Interpolating a linear field (should have zero error).
  - Interpolating points exactly on vertices, edges, and faces.
  - **Continuity Check:** Ensuring no jumps in value when moving between simplices.

## Tier 3: Scalability Benchmarks
- **Purpose:** Measure performance on large datasets.
- **Scope:**
  - Speedup measurements for systems with >100,000 query points.
  - Memory usage monitoring for the Parallel engine.

---

To run tests:
```bash
bash devtools/tests/run_tiers.sh smoke
```
