# Mathematical Foundations

LinDelInt relies on the concept of **Simplicial Interpolation** and **Orthogonal Projections**.

## 1. Barycentric Coordinates

For any point $\mathbf{P}$ inside a simplex (triangle in 2D, tetrahedron in 3D) with vertices $\mathbf{V}_0, \mathbf{V}_1, \dots, \mathbf{V}_n$, the point can be expressed as:
$$\mathbf{P} = \sum_{i=0}^n \lambda_i \mathbf{V}_i$$
where $\sum \lambda_i = 1$ and $\lambda_i \ge 0$.

The interpolated property $F(\mathbf{P})$ is then:
$$F(\mathbf{P}) = \sum_{i=0}^n \lambda_i F(\mathbf{V}_i)$$

## 2. Boundary Projections (Outside the Hull)

When a point lies outside the convex hull, LinDelInt performs a cascading search:

### Face Projection (3D)
The point is projected onto the plane of the closest boundary triangle. If the projected point lies within the triangle's 2D boundaries, the barycentric weights of that triangle are used.

### Edge Projection
If face projection fails, the point is projected onto the closest boundary edge. The property is linearly interpolated between the two edge vertices based on the projection factor $f \in [0, 1]$.

### Vertex Fallback
If both fail, the property of the closest vertex (calculated via KDTree) is assigned to the point.
