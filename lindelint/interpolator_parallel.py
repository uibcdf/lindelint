from scipy.spatial import Delaunay, KDTree
import numpy as np
import numpy.linalg as la
from numba import njit, prange

@njit(parallel=True)
def _do_your_thing_3d_numba(points, n_points, dim_properties, delaunay_simplices, delaunay_transform, 
                            properties, triangle, triangle_normal, b01_tri, b02_tri, inv_X_tri, aux_last_tri,
                            edge, u_edge, d_edge, op0_edge, op1_edge, vertex_points, vertex_indices):
    
    out_properties = np.zeros((n_points, dim_properties))
    done = np.zeros(n_points, dtype=np.bool_)

    # 1. Inside (Finding simplex must be done outside or via a Numba-compatible way)
    # Since find_simplex is not easily njit-able, we pass its results.
    
    # 2. Main Parallel Loop over points
    for jj in prange(n_points):
        point = points[jj]
        
        # --- PHASE 2: Triangles (Faces) ---
        if not done[jj]:
            for i in range(len(triangle)):
                p0 = vertex_points[triangle[i, 0]]
                p_to_p0 = point - p0
                
                # Condition: In front of normal
                if np.dot(p_to_p0, triangle_normal[i]) >= 0:
                    # Barycentric 2D projection
                    p_f = point - p0
                    pts_in_b = np.array([np.dot(p_f, b01_tri[i]), np.dot(p_f, b02_tri[i])])
                    
                    diff = pts_in_b - aux_last_tri[i]
                    b = inv_X_tri[i] @ diff
                    b2 = 1.0 - b[0] - b[1]
                    
                    if b[0] >= 0 and b[0] <= 1 and b[1] >= 0 and b[1] <= 1 and b2 >= 0 and b2 <= 1:
                        # Success
                        out_properties[jj] = b[0] * properties[triangle[i, 0]] + \
                                             b[1] * properties[triangle[i, 1]] + \
                                             b2   * properties[triangle[i, 2]]
                        done[jj] = True
                        break

        # --- PHASE 3: Edges ---
        if not done[jj]:
            for i in range(len(edge)):
                p0 = vertex_points[edge[i, 0]]
                p_to_p0 = point - p0
                
                if np.dot(p_to_p0, op0_edge[i]) >= 0 and np.dot(p_to_p0, op1_edge[i]) >= 0:
                    f = np.dot(p_to_p0, u_edge[i]) / d_edge[i]
                    if f >= 0 and f <= 1:
                        out_properties[jj] = (1.0 - f) * properties[edge[i, 0]] + f * properties[edge[i, 1]]
                        done[jj] = True
                        break
        
        # Corner fallback (KDTree) is handled in the wrapper due to complexity
    
    return out_properties, done

class InterpolatorParallel():
    """
    Ultra-high performance parallel CPU version of the Linear Delaunay Interpolator.
    Uses Numba JIT and multi-threading.
    """

    def __init__(self, points, properties):
        # We reuse the initialization logic from Vectorized as it's already optimized
        from lindelint.interpolator_vectorized import InterpolatorVectorized
        self._v_engine = InterpolatorVectorized(points, properties)
        self.points = self._v_engine.points
        self.properties = self._v_engine.properties
        self.dim = self._v_engine.dim
        self.n_points = self._v_engine.n_points
        self.dim_properties = self._v_engine.dim_properties

    def do_your_thing(self, query_points):
        if self.dim == 3:
            return self._do_your_thing_3d(query_points)
        elif self.dim == 2:
            # Fallback to vectorized for now, or implement 2D Numba
            return self._v_engine.do_your_thing(query_points)
        raise ValueError("Only 2D/3D supported.")

    def _do_your_thing_3d(self, query_points):
        n_q = query_points.shape[0]
        simplex_idx = self._v_engine.delaunay.find_simplex(query_points)
        
        # Initial pass for points INSIDE (Vectorized is already very fast here)
        properties = np.zeros((n_q, self.dim_properties))
        done = np.zeros(n_q, dtype=bool)
        
        inside = (simplex_idx != -1)
        if np.any(inside):
            s_idx = simplex_idx[inside]
            X = self._v_engine.delaunay.transform[s_idx, :3]
            Y = query_points[inside] - self._v_engine.delaunay.transform[s_idx, 3]
            b = np.einsum('ijk,ik->ij', X, Y)
            bcoords = np.column_stack([b, 1.0 - b.sum(axis=1)])
            properties[inside] = np.einsum('ij,ijk->ik', bcoords, self.properties[self._v_engine.delaunay.simplices[s_idx]])
            done[inside] = True

        # Parallel pass for points OUTSIDE (The heavy part)
        if not np.all(done):
            not_done_mask = ~done
            pts_nd = query_points # Pass all points, but Numba handles the 'done' check internally
            
            res_nd, done_nd = _do_your_thing_3d_numba(
                pts_nd, n_q, self.dim_properties, 
                self._v_engine.delaunay.simplices,
                self._v_engine.delaunay.transform,
                self.properties,
                self._v_engine.triangle,
                self._v_engine.triangle_outer_normal,
                self._v_engine.b01_tri,
                self._v_engine.b02_tri,
                self._v_engine.inv_X_tri,
                self._v_engine.aux_vertices_last,
                self._v_engine.edge,
                self._v_engine.u_edge,
                self._v_engine.d_edge,
                self._v_engine.outer_parallel_0,
                self._v_engine.outer_parallel_1,
                self.points, # vertex_points
                self._v_engine.vertex # vertex_indices
            )
            
            # Merge results (respecting what was already done inside)
            # Only update if Numba found a solution AND it wasn't already solved
            update_mask = done_nd & (~done)
            properties[update_mask] = res_nd[update_mask]
            done[update_mask] = True

        # Final pass: Corners (Vectorized KDTree is already fast)
        if not np.all(done):
            nd_indices = np.where(~done)[0]
            _, neighbor = self._v_engine.vertices_kdtree.query(query_points[nd_indices])
            properties[nd_indices] = self.properties[self._v_engine.vertex[neighbor]]
            done[nd_indices] = True

        return properties
