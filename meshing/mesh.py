import numpy as np
from . import Halfedge, Edge, Vertex, Face, Topology

"""
NOTE: We will NOT deal with boundary loops 
"""

class Mesh:
    def __init__(self, vertices, face_indices):
        self.vertices = vertices
        self.indices = face_indices 
        self.topology = Topology()
        self.topology.build(len(vertices), face_indices)

    def export_soup(self):
        init_n = len(self.vertices)
        face_conn = np.array(self.topology.export_face_connectivity(), dtype=np.uint32)
        edge_conn = np.array(self.topology.export_edge_connectivity(), dtype=np.uint32)

        old_inds = np.array(sorted(self.topology.vertices.keys()))
        new_inds = np.arange(len(old_inds), dtype=int)
        vertices = self.vertices[old_inds]
        A = np.zeros(init_n, dtype=np.uint32)
        A[old_inds] = new_inds

        face_conn = A[face_conn]
        edge_conn = A[edge_conn]
        return vertices, face_conn, edge_conn

    # TODO: Q4
    def get_3d_pos(self, v: Vertex):
        """ Given a vertex primitive, return the position coordinates """
        return self.vertices[v.index]

    # TODO: Q4
    def vector(self, h: Halfedge):
        """ Given a halfedge primitive, return the vector """
        #is this parameter h the index value of the halfedge
        he = self.topology.halfedges[h.index]
        start = self.get_3d_pos(he.vertex)
        end = self.get_3d_pos(he.next.vertex)
        return end - start

    # TODO: Q4
    def faceNormal(self, f: Face):
        """ Given a face primitive, compute the unit normal """
        he1 = f.halfedge
        he2 = he1.next
        vect1 = self.vector(he1)
        vect2 = self.vector(he2)
        normal = np.cross(vect1, vect2)
        # Normalize the normal to obtain the unit normal
        unit_normal = normal / np.linalg.norm(normal)
        return unit_normal
    
    # TODO: Q5
    def smoothMesh(self, n=5):
        """ Laplacian smooth mesh n times """
        from . import LaplacianSmoothing
        LaplacianSmoothing(self, n).apply()
        self.export_obj("p7_custom.obj")

    def edgeFlip(self, e_id):
        """ edgeflip the mesh at e_id """
        from . import EdgeFlip
        EdgeFlip(self, e_id).apply()
        self.export_obj("edge_flip.obj")

        
    def view(self):
        """ Mesh viewer using polyscope """
        import polyscope as ps 
        ps.init() 
        ps_mesh = ps.register_surface_mesh("mesh", self.vertices, self.indices, edge_width=1)
        ps.show() 
    
    def export_obj(self, path):
        vertices, faces, edges = self.export_soup()
        with open(path, 'w') as f:
            for vi, v in enumerate(vertices):
                f.write("v %f %f %f\n" % (v[0], v[1], v[2]))
            for face_id in range(len(faces) - 1):
                f.write("f %d %d %d\n" % (faces[face_id][0] + 1, faces[face_id][1] + 1, faces[face_id][2] + 1))
            f.write("f %d %d %d" % (faces[-1][0] + 1, faces[-1][1] + 1, faces[-1][2] + 1))
            for edge in edges:
                f.write("\ne %d %d" % (edge[0] + 1, edge[1] + 1))
