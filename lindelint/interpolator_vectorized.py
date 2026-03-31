from scipy.spatial import Delaunay, KDTree
import numpy as np
import numpy.linalg as la
import smonitor

class InterpolatorVectorized():
    """
    High-performance vectorized version of the Linear Delaunay Interpolator.
    """

    def __init__(self, points, properties):
        self.points = points
        self.dim = points.shape[1]
        self.n_points = points.shape[0]
        self.properties = properties
        self.dim_properties = properties.shape[1]
        self.delaunay = None

        if self.dim == 2:
            if self.n_points == 3:
                self.delaunay = Delaunay(self.points)
            elif self.n_points >= 4:
                self.delaunay = Delaunay(self.points, qhull_options='QJ')
        elif self.dim == 3:
            if self.n_points == 4:
                self.delaunay = Delaunay(self.points)
            elif self.n_points >= 5:
                self.delaunay = Delaunay(self.points, qhull_options='QJ')

        if self.delaunay is not None:
            # Telemetry: Mesh Stats
            smonitor.emit("lindelint.mesh.stats", 
                          level="DEBUG",
                          n_simplices=self.delaunay.nsimplex,
                          n_points=self.n_points)
            
            if self.delaunay.nsimplex == 0:
                smonitor.emit_from_catalog("LDL-W010", n_simplices=0, source="lindelint.InterpolatorVectorized")

            self.points = self.delaunay.points
            if self.dim == 3:
                self._prepare_3d_structures()
            elif self.dim == 2:
                self._prepare_2d_structures()

    def _prepare_3d_structures(self):
        self.triangle = self.delaunay.convex_hull
        self.n_triangles = self.triangle.shape[0]
        self.triangle_outer_normal = np.zeros((self.n_triangles, 3))
        self.b01_tri = np.zeros((self.n_triangles, 3))
        self.b02_tri = np.zeros((self.n_triangles, 3))
        self.inv_X_tri = np.zeros((self.n_triangles, 2, 2))
        self.aux_vertices_last = np.zeros((self.n_triangles, 2))
        edge_map = {}
        tetra_boundary = []
        for ii, neighbors in enumerate(self.delaunay.neighbors):
            if -1 in neighbors: tetra_boundary.append(self.delaunay.simplices[ii])
        tetra_boundary = np.array(tetra_boundary)

        for ii, tri in enumerate(self.triangle):
            p0, p1, p2 = self.points[tri[0]], self.points[tri[1]], self.points[tri[2]]
            for tetra in tetra_boundary:
                if np.all(np.isin(tri, tetra)):
                    interior_vertex = np.setdiff1d(tetra, tri)[0]
                    normal = np.cross(p1 - p0, p2 - p0)
                    normal /= la.norm(normal)
                    if np.dot(self.points[interior_vertex] - p0, normal) > 0: normal = -normal
                    self.triangle_outer_normal[ii] = normal
                    break
            v01 = p1 - p0
            d01 = la.norm(v01)
            b01 = v01 / d01
            self.b01_tri[ii] = b01
            v02 = p2 - p0
            b02 = v02 - np.dot(v02, b01) * b01
            b02 /= la.norm(b02)
            self.b02_tri[ii] = b02
            v01_in_b = [np.dot(v01, b01), 0.0]
            v02_in_b = [np.dot(v02, b01), np.dot(v02, b02)]
            self.aux_vertices_last[ii] = v02_in_b
            X = np.column_stack([np.array(v01_in_b) - v02_in_b, np.array(v02_in_b) - v02_in_b]) # Logic fix: based on original pedal
            # Re-implementing exact pedal logic for parity
            aux_vertices = np.array([[0.0, 0.0], v01_in_b, v02_in_b])
            self.aux_vertices_last[ii] = aux_vertices[-1]
            X = (aux_vertices[:-1] - aux_vertices[-1]).T
            self.inv_X_tri[ii] = la.inv(X)
            for pair in [(0,1), (0,2), (1,2)]:
                e = tuple(sorted((tri[pair[0]], tri[pair[1]])))
                if e not in edge_map: edge_map[e] = []
                edge_map[e].append(ii)
        self.edge = np.array(list(edge_map.keys()))
        self.n_edges = self.edge.shape[0]
        self.u_edge = np.zeros((self.n_edges, 3))
        self.d_edge = np.zeros(self.n_edges)
        self.outer_parallel_0 = np.zeros((self.n_edges, 3))
        self.outer_parallel_1 = np.zeros((self.n_edges, 3))
        for i, e in enumerate(self.edge):
            p0, p1 = self.points[e[0]], self.points[e[1]]
            v01 = p1 - p0
            d01 = la.norm(v01)
            self.d_edge[i] = d01
            u01 = v01 / d01
            self.u_edge[i] = u01
            tris = edge_map[tuple(e)]
            if len(tris) >= 2:
                n0 = self.triangle_outer_normal[tris[0]]
                op0 = np.cross(n0, u01); op0 /= la.norm(op0)
                opp_v0 = np.setdiff1d(self.triangle[tris[0]], e)[0]
                if np.dot(self.points[opp_v0] - p0, op0) > 0: op0 = -op0
                self.outer_parallel_0[i] = op0
                n1 = self.triangle_outer_normal[tris[1]]
                op1 = np.cross(n1, u01); op1 /= la.norm(op1)
                opp_v1 = np.setdiff1d(self.triangle[tris[1]], e)[0]
                if np.dot(self.points[opp_v1] - p0, op1) > 0: op1 = -op1
                self.outer_parallel_1[i] = op1
        self.vertex = np.unique(self.edge)
        self.vertices_kdtree = KDTree(self.points[self.vertex])

    def _prepare_2d_structures(self):
        self.triangle = []
        for ii, neighbors in enumerate(self.delaunay.neighbors):
            if -1 in neighbors: self.triangle.append(self.delaunay.simplices[ii])
        self.triangle = np.array(self.triangle)
        self.edge = self.delaunay.convex_hull
        self.n_edges = self.edge.shape[0]
        self.edge_outer_normal = np.zeros((self.n_edges, 2))
        self.u_edge = np.zeros((self.n_edges, 2))
        self.d_edge = np.zeros(self.n_edges)
        for i, e in enumerate(self.edge):
            p0, p1 = self.points[e[0]], self.points[e[1]]
            v01 = p1 - p0
            d01 = la.norm(v01); self.d_edge[i] = d01
            u01 = v01 / d01; self.u_edge[i] = u01
            for tri in self.triangle:
                if np.all(np.isin(e, tri)):
                    opp_v = np.setdiff1d(tri, e)[0]
                    normal = np.array([u01[1], -u01[0]])
                    if np.dot(self.points[opp_v] - p0, normal) > 0: normal = -normal
                    self.edge_outer_normal[i] = normal
                    break
        self.vertex = np.unique(self.edge)
        self.vertices_kdtree = KDTree(self.points[self.vertex])

    def do_your_thing(self, points):
        if self.dim == 2: return self._do_your_thing_2d_vectorized(points)
        if self.dim == 3: return self._do_your_thing_3d_vectorized(points)
        return None

    def _do_your_thing_3d_vectorized(self, points):
        n_points = points.shape[0]
        properties = np.zeros((n_points, self.dim_properties))
        done = np.zeros(n_points, dtype=bool)
        stats = {"inside": 0, "triangles": 0, "edges": 0, "corners": 0}

        simplex_idx = self.delaunay.find_simplex(points)
        inside = (simplex_idx != -1)
        if np.any(inside):
            s_idx = simplex_idx[inside]
            X = self.delaunay.transform[s_idx, :3]
            Y = points[inside] - self.delaunay.transform[s_idx, 3]
            b = np.einsum('ijk,ik->ij', X, Y)
            bcoords = np.column_stack([b, 1.0 - b.sum(axis=1)])
            properties[inside] = np.einsum('ij,ijk->ik', bcoords, self.properties[self.delaunay.simplices[s_idx]])
            done[inside] = True
            stats["inside"] = int(np.sum(inside))

        for i in range(self.n_triangles):
            not_done = ~done
            if not np.any(not_done): break
            pts = points[not_done]
            p0 = self.points[self.triangle[i, 0]]
            in_front = np.dot(pts - p0, self.triangle_outer_normal[i]) >= 0
            if not np.any(in_front): continue
            pts_f = pts[in_front]
            pts_in_b = np.stack([np.dot(pts_f - p0, self.b01_tri[i]), np.dot(pts_f - p0, self.b02_tri[i])], axis=1)
            b = np.einsum('jk,ik->ij', self.inv_X_tri[i], pts_in_b - self.aux_vertices_last[i])
            bcoords = np.column_stack([b, 1.0 - b.sum(axis=1)])
            valid = np.all((bcoords >= 0) & (bcoords <= 1), axis=1)
            if np.any(valid):
                idx = np.where(not_done)[0][in_front][valid]
                properties[idx] = np.einsum('ij,jk->ik', bcoords[valid], self.properties[self.triangle[i]])
                done[idx] = True
                stats["triangles"] += int(np.sum(valid))

        for i in range(self.n_edges):
            not_done = ~done
            if not np.any(not_done): break
            if la.norm(self.outer_parallel_0[i]) == 0: continue
            pts = points[not_done]; p0 = self.points[self.edge[i, 0]]
            mask = (np.dot(pts - p0, self.outer_parallel_0[i]) >= 0) & (np.dot(pts - p0, self.outer_parallel_1[i]) >= 0)
            if not np.any(mask): continue
            f = np.dot(pts[mask] - p0, self.u_edge[i]) / self.d_edge[i]
            valid = (f >= 0) & (f <= 1)
            if np.any(valid):
                idx = np.where(not_done)[0][mask][valid]
                f_v = f[valid][:, np.newaxis]
                properties[idx] = (1.0 - f_v) * self.properties[self.edge[i, 0]] + f_v * self.properties[self.edge[i, 1]]
                done[idx] = True
                stats["edges"] += int(np.sum(valid))

        not_done = ~done
        if np.any(not_done):
            idx = np.where(not_done)[0]
            _, neighbor = self.vertices_kdtree.query(points[idx])
            properties[idx] = self.properties[self.vertex[neighbor]]
            done[idx] = True
            stats["corners"] = int(np.sum(not_done))

        smonitor.emit("lindelint.interpolator.breakdown", level="DEBUG", **stats)
        return properties

    def _do_your_thing_2d_vectorized(self, points):
        # Similar logic for 2D with breakdown...
        return self._do_your_thing_3d_vectorized(points) # placeholder for consistency
