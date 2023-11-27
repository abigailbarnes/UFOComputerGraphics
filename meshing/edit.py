from . import Halfedge, Edge, Vertex, Face, Topology, Mesh
import numpy as np


class MeshEdit():
    def __init__(self):
        pass

    def apply(self):
        raise NotImplementedError()

    def inverse(self):
        raise NotImplementedError()

class LaplacianSmoothing(MeshEdit):
    def __init__(self, mesh: Mesh, n_iter: int):
        self.mesh = mesh
        self.n_iter = n_iter
    
    def _apply(self): 
        for iteration in range(self.n_iter):
            newpositions = []
            #print(type(self.mesh.vertices))
            for vertex in self.mesh.topology.vertices.values():
                #print("AHHHH")
                #print(type(val))
                adjv = vertex.adjacentVertices()
                #print(adjv)
                averagex = 0
                averagey = 0
                averagez = 0
                for adjacent in adjv:
                    position = self.mesh.get_3d_pos(adjacent)
                    #print(type(position))
                    averagex += position[0]
                    averagey += position[1]
                    averagez += position[2]
                    #print(averagex, averagey, averagez)
                averagex /= len(adjv)
                averagey /= len(adjv)
                averagez /= len(adjv)
                posave = np.array([averagex, averagey, averagez])
                #newpositions[vertex.index] = posave
                newpositions.append(posave)
                #print(type(posave))
                #print(averagex, averagey, averagez)
            self.mesh.vertices = np.array(newpositions)

            
        #for item in self.mesh.topology.vertices.items():
            #print(item)
        return True 

    def apply(self):
        return self._apply()

# TODO: Q4 -- complete this 
class EdgeCollapse(MeshEdit):
    def __init__(self, mesh: Mesh, e_id: int):
        self.mesh = mesh
        self.e_id = e_id

    def apply(self):
        return next(do_collapse(self.mesh, self.e_id))
  
# TODO: Q4 -- complete this 
def do_collapse(mesh, e_id):
    topology = mesh.topology
    #initializations
    #what do we actually do with the following stuff
    #do we need to delete this edge from topology edges?
    e = topology.edges[e_id]
    yield True
    
  
# TODO: Extra credit -- complete this 
class EdgeCollapseWithLink(MeshEdit):
    def __init__(self, mesh: Mesh, e_id: int):
        self.mesh = mesh
        self.e_id = e_id
        event = do_collapse_with_link(mesh, e_id)
        self.do_able = next(event)
        if self.do_able is False:
            return
        self.event = event

    def apply(self):
        return next(self.event)

# TODO: Extra credit -- complete this 
def do_collapse_with_link(mesh, e_id):
    topology = mesh.topology
    e = topology.edges[e_id]
    yield True






class EdgeFlip(MeshEdit):
    def __init__(self, mesh: Mesh, e_id: int):
        self.mesh = mesh
        self.e_id = e_id
    
    def _apply(self): 
        topology = self.mesh.topology
        edge = topology.edges[self.e_id]
        he = edge.halfedge
        #print(he)
        #print(type(he))
        #reference affected half edges
        #print('here woop woop')
        he5 = he.next.next
        #print(type(he5))
        he4 = he.next
        #print(type(he4))
        twin = he.twin
        he1 = twin.next.next
        he0 = twin.next

        #ensure that no face or vertex references to the current he or twin
        he0.vertex.halfedge = he0
        he1.vertex.halfedge = he1
        he4.vertex.halfedge = he4
        he5.vertex.halfedge = he5

        #print(type(he1))
        he1.face.halfedge = he1
        he5.face.halfedge = he5
        
        #updating the diagonal
        he.next = he5
        he.next.next = he0
        he.vertex = he1.vertex
        he.face = he5.face
        twin.next = he1
        twin.next.next = he4
        twin.vertex = he5.vertex
        twin.face = he1.face

        #update affected next and prev references
        he0.next = he
        he1.next = he4
        he4.next = twin
        he5.next = he0

        he0.next.next = he5
        he1.next.next = twin
        he4.next.next = he1
        he5.next.next = he
        
        return True 

    def apply(self):
        return self._apply()
