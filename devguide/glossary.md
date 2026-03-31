# Glossary

To ensure clarity, LinDelInt uses the following definitions:

| Term | Definition |
| :--- | :--- |
| **Simplex** | The simplest polytope possible in a given dimension (Triangle in 2D, Tetrahedron in 3D). |
| **Convex Hull** | The smallest convex set that contains all the base points. Points outside this set require projection. |
| **Delaunay Triangulation** | A triangulation such that no point is inside the circumcircle of any simplex. |
| **Barycentric Coordinates** | A coordinate system where the position of a point is defined relative to the vertices of a simplex. |
| **Query Point** | A point where the value of a property needs to be estimated via interpolation. |
| **Kernel Fusion** | The optimization technique of combining multiple operations into a single compiled loop (used in the Parallel engine). |
