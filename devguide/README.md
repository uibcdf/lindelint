# LinDelInt Developer Guide

Welcome to the **LinDelInt** (Linear Delaunay Interpolator) developer guide. This document serves as the technical reference for the library's architecture and standards.

## Vision

LinDelInt is the high-performance interpolation engine for the **MolSysSuite**. It provides robust, physically-consistent linear interpolation based on Delaunay triangulation, specifically designed to handle molecular trajectories and volumetric data.

## Guiding Principles

- **Efficiency:** Core interpolation logic must be vectorized (NumPy) to handle large coordinate sets.
- **Robustness:** Proper handling of points outside the convex hull via projection.
- **Dimensional Consistency:** Use `pyunitwizard` for all physical coordinates.
- **Ecosystem Alignment:** Follow the `SMonitor`, `ArgDigest`, and `DepDigest` standards.

## Table of Contents

- [Architecture](architecture.md): Internal logic and triangulation.
- [Vectorization Plan](vectorization.md): Comparison between original and vectorized engines.
- [SMonitor Integration](smonitor_integration.md): Diagnostic codes and signals.
- [Testing Strategy](testing_strategy.md): Tiers of verification.
