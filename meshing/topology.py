import numpy as np
from collections import defaultdict
from . import Halfedge, Vertex, Edge, Face

class ElemCollection(dict):
    """This dict wrapper keeps track of the number of uniquly allocated elements
    so that each element has an unambiguous id in the lifetime of the mesh (even after edits)
    """
    def __init__(self, cons_f):
        super().__init__()
        self.cons_f = cons_f
        self.n_allocations = 0

    def allocate(self):
        elem = self.cons_f()
        i = self.n_allocations
        elem.index = i
        self[i] = elem
        self.n_allocations += 1
        return elem

    def fill_vacant(self, elem_id):
        """an element was previously deleted, and is now re-inserted"""
        assert elem_id not in self
        elem = self.cons_f()
        elem.index = elem_id
        self[elem_id] = elem
        return elem

    def compactify_keys(self):
        """fill the holes in index keys"""
        store = dict()
        for i, (_, elem) in enumerate(sorted(self.items())):
            store[i] = elem
            elem.index = i
        self.clear()
        self.update(store)

class Topology():
    def __init__(self):
        self.halfedges = ElemCollection(Halfedge)
        self.vertices = ElemCollection(Vertex)
        self.edges = ElemCollection(Edge)
        self.faces = ElemCollection(Face)

    def build(self, n_vertices, indices) -> bool:
        # TODO: Q1 -- complete this function  
        """
        This will be the primary function for generating your halfedge data structure. As the name suggests, the central element of 
        this data structure will be the Halfedge. Halfedges are related to each other through two operations `twin` and `next`. 
        Halfedge.twin returns the halfedge the shares the same edge as the current Halfedge, but is oppositely oriented
        (e.g. if halfedge H points from vertex A to vertex B, then H.twin points from vertex B to vertex A). Halfedge.next returns the
        next halfedge within the same triangle in the same orientation (e.g. given triangle ABC, if halfedge H goes A->B, then H.next 
        goes B -> C). With these properties alone, every halfedge can be associated with a specific face, vertex, and edge. Thus, in 
        your implementation every halfedge H should be assigned a Face, Vertex, and Edge element as attributes. Likewise, every Face, 
        Vertex, and Edge element should be assigned a halfedge H. Note that this relationship is not 1:1, so that there are multiple valid
        halfedges you can assign to Face, Vertex, and Edge. The choice is not important. As long as the orientation of the elements are 
        consistent across the mesh, then your implementation should work. 
        
        ======== VERY IMPORTANT =======
        In order for your implementation to pass our checks, you MUST allocate faces/halfedges in the following order 
        for {face array} in `indices` array:
            - If a {face array} contains vertex indices [i,j,k], then allocate halfedges/edges in the order (i,j), (j,k), (k, i)
            - If an edge has already been encountered, then set the new halfedge as the `twin` of the existing halfedge 
        """

        visited = {}

        for i in range(n_vertices):
            self.vertices.allocate()

        for face in indices:
            f = self.faces.allocate()

            hes = []

            for i in range(3):
                he = self.halfedges.allocate()
                hes.append(he)
            
            #for he in hes:
                #print(he)

            #print(face)

            #looping through each of the three values in the face array
            for i in range(3):
                #print(hes)
                he = hes[i]
                #print(type(he))
                he.next = hes[(i + 1) % 3]
                v = self.vertices[face[i]]
                v.halfedge = he
                f.halfedge = he
                he.face = f
                he.vertex = v

                v1 = face[i]
                v2 = face[(i + 1) % 3]

                if(v1 <= v2):
                        endpoints = (v1, v2)
                else:
                    endpoints = (v2, v1)

                #if the edge has already been visited
                if(endpoints in visited):
                    existingedge = visited[endpoints] 
                    existingedge.halfedge.twin = he
                    he.twin = existingedge.halfedge
                    he.edge = existingedge
                    #print("here")

                #if the edge has NOT already been visited
                else:
                    e = self.edges.allocate()
                    he.edge = e
                    e.halfedge = he
                    visited[endpoints] = e



                
        #print(self.hasNonManifoldEdges())
        #print(self.hasNonManifoldVertices())
        #self.thorough_check()
        return True

    def compactify_keys(self):
        self.halfedges.compactify_keys()
        self.vertices.compactify_keys()
        self.edges.compactify_keys()
        self.faces.compactify_keys()

    def export_halfedge_serialization(self):
        """
        this provides the unique, unambiguous serialization of the halfedge topology
        i.e. one can reconstruct the mesh connectivity from this information alone
        It can be used to track history, etc.
        """
        data = []
        for _, he in sorted(self.halfedges.items()):
            data.append(he.serialize())
        data = np.array(data, dtype=np.int32)
        return data

    def export_face_connectivity(self):
        face_indices = []
        for inx, face in self.faces.items():
            vs_of_this_face = []
            if face.halfedge is None:
                continue
            for vtx in face.adjacentVertices():
                vs_of_this_face.append(vtx.index)
            assert len(vs_of_this_face) == 3
            face_indices.append(vs_of_this_face)
        return face_indices

    def export_edge_connectivity(self):
        conn = []
        for _, edge in self.edges.items():
            if edge.halfedge is None:
                continue
            v1 = edge.halfedge.vertex
            v2 = edge.halfedge.twin.vertex
            conn.append([v1.index, v2.index])
        return conn

    def hasNonManifoldVertices(self):
        # TODO: Q3 -- return True if any non-manifold vertices found, False otherwise
        actual = {}
        expected = {}
        #print(self.faces)
        for i in range(len(self.faces)):
            vertices = self.faces[i].adjacentVertices()
            #print(vertices)
            #looping through each face that is currently contained in the mesh
            #print(self.faces[i])
            #print(type(self.faces[i]))
            #print(self.faces[i])
            #adjv = self.faces[i].adjacentVertices()
            adjf = self.faces[i].adjacentFaces()
            #print(len(adjv), len(adjf))
            #print(adjf)
            #print(type(adjf[1]))
            for j in range(len(vertices)):
                vertex = vertices[j]
                #print(vertex)
                if(vertex in actual):
                    actual[vertex] += 1
                    if(actual[vertex] > vertex.degree()):
                        #print("here")
                        return True
                else:
                    actual[vertex] = 1
                
                #print(vertex.degree())
                #expected[vertex] = vertex.degree
            '''for j in range(len(adjv)):
                currv = adjv[j]
                if(currv in verticefaces):
                    verticefaces[currv] += 1
                else:
                    verticefaces[currv] = 1'''
            
            #FINISH: compare the number of adjacent vertices to the number of faces that contain that vertice to be equal
        return False
    
    def hasNonManifoldEdges(self):
        # TODO: Q3 -- return True if any non-manifold edges found, False otherwise 
        #print(self.faces)
        edges = {}

        #print(type(self.halfedges))
        #print(len(self.halfedges))
        #print(self.halfedges)
        
        for i in range(len(self.halfedges)):
            #print(i)
            #print(type(self.halfedges[i]))
            edge = self.halfedges[i].edge
            #print(edge)
            if(edge in edges):
                #print("here")
                #print(edges[edge])
                edges[edge] += 1
                if(edges[edge] > 2):
                    return True
                #print(edges[edge])
            else:
                edges[edge] = 1
        #print(edges)

        return False

    '''def thorough_check(self):
        # Check full halfedge coverage across all mesh elements  
        if len(self.halfedges) == 0 or len(self.vertices) == 0 or len(self.faces) == 0 or len(self.edges) == 0: 
            print(f"Warning: Topology is incomplete. You need to allocate halfedge, vertex, face, and edge elements in order for the checker to work.")
            return 
            
        def check_indexing(src_dict):
            for inx, v in src_dict.items():
                assert inx == v.index

        check_indexing(self.halfedges)
        check_indexing(self.vertices)
        check_indexing(self.edges)
        check_indexing(self.faces)

        # 2. check edges
        self._check_verts()
        self._check_edges()
        self._check_faces()'''
  
    def _check_verts(self):
        encountered_halfedges = []
        for inx, v in self.vertices.items():
            hes = []
            for he in v.adjacentHalfedges():
                # if he.vertex != v:
                #     return False, he, v
                assert he.vertex == v
                hes.append(he)
            encountered_halfedges.extend([elem.index for elem in hes])
        encountered_halfedges = set(encountered_halfedges)
        assert encountered_halfedges == set(self.halfedges.keys()), "must cover all halfedges"
        # return True, True, True
    def _check_edges(self):
        encountered_halfedges = []
        for inx, e in self.edges.items():
            he = e.halfedge
            twin = he.twin

            hes = [he, twin]
            n = len(hes)

            for i, he in enumerate(hes):
                assert he.edge == e
                assert he.twin == hes[(i + 1) % n]

            encountered_halfedges.extend([elem.index for elem in hes])

        encountered_halfedges = set(encountered_halfedges)
        assert encountered_halfedges == set(self.halfedges.keys()), "must cover all halfedges"

    def _check_faces(self):
        encountered_halfedges = []
        for inx, f in self.faces.items():
            hes = []
            for he in f.adjacentHalfedges():
                hes.append(he)

            n = len(hes)
            for i, he in enumerate(hes):
                assert he.face == f
                assert he.next == hes[(i + 1) % n]

            encountered_halfedges.extend([elem.index for elem in hes])

        encountered_halfedges = set(encountered_halfedges)
        target_halfedges = {
            k for k, v in self.halfedges.items()
        }
        assert encountered_halfedges == target_halfedges, \
            f"must cover all halfedges"