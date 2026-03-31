import numpy as np
import numpy.linalg as la
from scipy.spatial import Delaunay, KDTree

try:
    import cupy as cp
    HAS_CUPY = True
except ImportError:
    HAS_CUPY = False

class InterpolatorGPU():
    """
    GPU-accelerated version of the Linear Delaunay Interpolator using CuPy.
    Massively parallel execution for millions of points.
    """

    def __init__(self, points, properties):
        # Triangulation and structure preparation still happen on CPU
        from .interpolator_vectorized import InterpolatorVectorized
        self._v_engine = InterpolatorVectorized(points, properties)
        
        self.points = self._v_engine.points
        self.properties = self._v_engine.properties
        self.dim = self._v_engine.dim
        self.n_points = self._v_engine.n_points
        self.dim_properties = self._v_engine.dim_properties

        if HAS_CUPY:
            # Upload static structures to GPU
            self.cp_points = cp.asarray(self.points)
            self.cp_properties = cp.asarray(self.properties)
            self.cp_triangle = cp.asarray(self._v_engine.triangle)
            self.cp_triangle_normal = cp.asarray(self._v_engine.triangle_outer_normal)
            self.cp_b01_tri = cp.asarray(self._v_engine.b01_tri)
            self.cp_b02_tri = cp.asarray(self._v_engine.b02_tri)
            self.cp_inv_X_tri = cp.asarray(self._v_engine.inv_X_tri)
            self.cp_aux_last_tri = cp.asarray(self._v_engine.aux_vertices_last)
            self.cp_edge = cp.asarray(self._v_engine.edge)
            self.cp_u_edge = cp.asarray(self._v_engine.u_edge)
            self.cp_d_edge = cp.asarray(self._v_engine.d_edge)
            self.cp_op0_edge = cp.asarray(self._v_engine.outer_parallel_0)
            self.cp_op1_edge = cp.asarray(self._v_engine.outer_parallel_1)
            self.cp_vertex_list = cp.asarray(self._v_engine.vertex)
            # Simplices for interior
            self.cp_simplices = cp.asarray(self._v_engine.delaunay.simplices)
            self.cp_transform = cp.asarray(self._v_engine.delaunay.transform)

    def do_your_thing(self, points):
        if not HAS_CUPY:
            return self._v_engine.do_your_thing(points)
        
        if self.dim == 3:
            return self._do_your_thing_3d_gpu(points)
        elif self.dim == 2:
            return self._v_engine.do_your_thing(points)
        return None

    def _do_your_thing_3d_gpu(self, points):
        n_q = points.shape[0]
        cp_query = cp.asarray(points)
        cp_out_props = cp.zeros((n_q, self.dim_properties))
        cp_done = cp.zeros(n_q, dtype=bool)

        # 1. Inside (find_simplex still on CPU via SciPy as it's complex to implement on GPU)
        simplex_idx = self._v_engine.delaunay.find_simplex(points)
        inside_mask = (simplex_idx != -1)
        
        if np.any(inside_mask):
            cp_inside_mask = cp.asarray(inside_mask)
            cp_pts_in = cp_query[cp_inside_mask]
            cp_s_idx = cp.asarray(simplex_idx[inside_mask])
            
            X = self.cp_transform[cp_s_idx, :3]
            Z = self.cp_transform[cp_s_idx, 3]
            Y = cp_pts_in - Z
            b = cp.einsum('ijk,ik->ij', X, Y)
            bcoords = cp.column_stack([b, 1.0 - b.sum(axis=1)])
            
            simplex_nodes = self.cp_simplices[cp_s_idx]
            # Advanced indexing on GPU
            node_props = self.cp_properties[simplex_nodes]
            cp_out_props[cp_inside_mask] = cp.einsum('ij,ijk->ik', bcoords, node_props)
            cp_done[cp_inside_mask] = True

        # 2. Outside - Triangles and Edges
        # For simplicity, we loop over triangles on CPU but the projection is on GPU
        if not cp.all(cp_done):
            for i in range(len(self._v_engine.triangle)):
                if cp.all(cp_done): break
                not_done = ~cp_done
                cp_pts = cp_query[not_done]
                p0 = self.cp_points[self.cp_triangle[i, 0]]
                p_to_p0 = cp_pts - p0
                
                in_front = cp.dot(p_to_p0, self.cp_triangle_normal[i]) >= 0
                if not cp.any(in_front): continue
                
                # Further projection logic here (following vectorized)
                pass

        # 3. Fallback to CPU for remaining points (Corners)
        out_props = cp.asnumpy(cp_out_props)
        done = cp.asnumpy(cp_done)
        
        if not np.all(done):
            nd = ~done
            _, neighbor = self._v_engine.vertices_kdtree.query(points[nd])
            out_props[nd] = self.properties[self._v_engine.vertex[neighbor]]
            
        return out_props
