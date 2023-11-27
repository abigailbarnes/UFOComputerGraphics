class Primitive():
    def __init__(self):
        self.halfedge = None
        self.index = -1

    def __str__(self) -> str:
        return str(self.index)

    def __repr__(self) -> str:
        return str(self)


class Halfedge(Primitive):
    def __init__(self):
        # note parent constructor is replaced
        self.vertex = None
        self.edge = None
        self.face = None
        # self.corner = None
        self.next = None
        self.twin = None
        self.index = -1  # an ID between 0 and |H| - 1, where |H| is the number of halfedges in a mesh

    def prev(self):
        # TODO: Q2 -- complete this function
        """ Return previous halfedge """
        heprev = self.next.next
        return heprev

    def tip_vertex(self):
        # TODO: Q2 -- complete this function
        """ Return vertex on the tip of the halfedge """
        vtip = self.next.vertex
        return vtip

    def serialize(self):
        return (
            self.index,
            self.vertex.index,
            self.edge.index,
            self.face.index,
            self.next.index,
            self.twin.index,
        )


class Edge(Primitive):
    """ initialization: assign halfedge and index (see Primitive) """
    
    def two_vertices(self):
        # TODO: Q2 -- complete this function
        """return the two incident vertices of the edge
        note that the incident vertices are ambiguous to ordering
        """
        #self is an edge
        he1 = self.halfedge.vertex
        he2 = self.halfedge.next.vertex

        return (he1, he2)


class Face(Primitive):
    """ initialization: assign halfedge and index (see Primitive) """
    def adjacentHalfedges(self):
        # TODO: Q2 -- complete this function
        # Return ONLY the halfedges for which this face is assigned to. Be careful not to return the twins! 
        """ Return iterator of adjacent halfedges """
        '''headj = []
        for he in self.halfedgs:
            if he.halfedge == self:
                headj.append(he)
        return headj'''

        hes = []
        oghe = self.halfedge
        hes.append(oghe)

        he = self.halfedge.next

        while he != oghe:
            hes.append(he)
            he = he.next

        return hes



    def adjacentVertices(self):
        # TODO: Q2 -- complete this function
        # Return all the vertices which are contained in this face 
        """ Return iterator of adjacent vertices """

        hes = [] 
        oghe = self.halfedge
        hes.append(oghe.vertex)

        he = self.halfedge.next

        while he != oghe:
            hes.append(he.vertex)
            he = he.next

        return hes

    def adjacentEdges(self):
        # TODO: Q2 -- complete this function
        # Return all the edges which make up this face 
        """ Return iterator of adjacent edges """
        hes = [] 
        oghe = self.halfedge
        hes.append(oghe.edge)

        he = self.halfedge.next

        while he != oghe:
            hes.append(he.edge)
            he = he.next

        return hes
    
    def adjacentFaces(self):
        # TODO: Q2 -- complete this function
        # Return all the faces which share an edge with this face
        """ Return iterator of adjacent faces """

        faces = []

        oghe = self.halfedge

        faces.append(oghe.face)

        he = self.halfedge.next

        while he != oghe:
            faces.append(he.twin.face)
            he = he.next

        return faces

class Vertex(Primitive):
    """ initialization: assign halfedge and index (see Primitive) """
    
    def degree(self):
        # TODO: Q2 -- complete this function
        """ Return vertex degree: # of incident edges """
        
        counter = 0

        oghe = self.halfedge
        counter += 1

        he = self.halfedge.twin.next

        while he != oghe:
            counter += 1
            he = he.twin.next

        return counter

    def isIsolated(self) -> bool:
        return self.halfedge is None

    def adjacentHalfedges(self):
        # TODO: Q2 -- complete this function
        # Return ONLY the halfedges for which this vertex is assigned to. Be careful not to return the twins! 
        """ Return iterator of adjacent halfedges """
        

        hes = []

        oghe = self.halfedge
        hes.append(self.halfedge)

        #print(oghe.next)
        #print(self.halfedge.next.twin)

        he = self.halfedge.twin.next

        while he != oghe:
            hes.append(he)
            he = he.twin.next
        
        return hes
    
    def adjacentVertices(self):
        # TODO: Q2 -- complete this function
        # Return all the vertices which are connected to this vertex by an edge 
        """ Return iterator of adjacent vertices """
        connected = []

        oghe = self.halfedge
        connected.append(self.halfedge.next.vertex)

        he = self.halfedge.twin.next

        while he != oghe:
            connected.append(he.next.vertex)
            he = he.twin.next
        
        return connected

    def adjacentEdges(self):
        #print("in adjacent edges")
        # TODO: Q2 -- complete this function
        # Return all the edges which this vertex is contained in 
        """ Return iterator of adjacent edges """

        edges = []

        oghe = self.halfedge
        edges.append(self.halfedge.next.edge)

        he = self.halfedge.twin.next

        while he != oghe:
            edges.append(he.next.edge)
            he = he.twin.next

        print('almost done with adj edges')
        
        return edges
    
    def adjacentFaces(self):
        # TODO: Q2 -- complete this function
        # Return all the faces which this vertex is contained in 
        """ Return iterator of adjacent faces """
        
        faces = []

        oghe = self.halfedge
        faces.append(self.halfedge.next.face)

        he = self.halfedge.twin.next

        while he != oghe:
            faces.append(he.next.face)
            he = he.twin.next
        
        return faces
