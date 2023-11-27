from meshing.io import PolygonSoup
from meshing.mesh import Mesh 

if __name__ == "__main__":
    # Initializes a PolygonSoup object from an obj file, which reads in the obj and fills out attributes vertices and indices (triangle faces)
    soup = PolygonSoup.from_obj("spot.obj")
    # Initialize your mesh object 
    mesh = Mesh(soup.vertices, soup.indices) 
    #mesh.view()
    '''print(mesh.topology.edges[3].halfedge)
    print(mesh.topology.edges[3].halfedge.next)
    print(mesh.topology.edges[3].halfedge.prev())

    print(mesh.topology.edges[10].halfedge)
    print(mesh.topology.edges[10].halfedge.next)
    print(mesh.topology.edges[10].halfedge.prev())

    print(mesh.topology.edges[100].halfedge)
    print(mesh.topology.edges[100].halfedge.next)
    print(mesh.topology.edges[100].halfedge.prev())

    #mesh.edgeFlip(3)
    #mesh.edgeFlip(10)
    #mesh.edgeFlip(100)

    print(mesh.topology.edges[3].halfedge)
    print(mesh.topology.edges[3].halfedge.next)
    print(mesh.topology.edges[3].halfedge.prev())

    print(mesh.topology.edges[10].halfedge)
    print(mesh.topology.edges[10].halfedge.next)
    print(mesh.topology.edges[10].halfedge.prev())

    print(mesh.topology.edges[100].halfedge)
    print(mesh.topology.edges[100].halfedge.next)
    print(mesh.topology.edges[100].halfedge.prev())'''
    #mesh.view() 

    #mesh.edgeFlip(3)
    #mesh.edgeFlip(10)
    #mesh.edgeFlip(100)

    flips = []
    he = 0
    #print(len(mesh.topology.edges))
    while he < len(mesh.topology.edges):
        flips.append(he)
        he += 100
    
    #print(len(flips))

    for flip in flips:
        #print(flip)
        mesh.edgeFlip(flip)
    
    '''
    # This is the checker function that is called at the end of topology.build() 
    # Currently, this will throw a warning. It will work once you actually start implementing topology.build(). 
    #mesh.topology.thorough_check()
    '''
    '''
    # NOTE: THE BELOW WILL NOT WORK UNTIL YOU ACTUALLY BEGIN WORKING THROUGH Q1/Q2 AND IMPLEMENT THE APPROPRIATE FUNCTIONS/ATTRIBUTE
     
    # Examples of some of the accessor functions you need to implement for Q2, along with how you can visualize/check them 
    # Get first halfedge in mesh 
    h = mesh.topology.halfedges[100].next
    # Previous of next halfedge is just original halfedge 
    assert h == h.next.prev() 
    # Tip vertex of the halfedge is the primary vertex of the twin 
    assert h.tip_vertex() == h.twin.vertex 
    
    # Highlight the faces associated with the current halfege and its twin 
    twin_face = h.twin.face 
    import polyscope as ps 
    import numpy as np 
    ps.init()
    # This initializes a mesh object to view in Polyscope 
    ps_mesh = ps.register_surface_mesh("mesh", soup.vertices, soup.indices)
    face_scalars = np.zeros(len(soup.indices))
    face_scalars[twin_face.index] = 1 
    face_scalars[h.face.index] = 2
    # This assigns our scalar array to colors chosen by Polyscope defined over the mesh faces 
    ps_mesh.add_scalar_quantity('halfedge faces', face_scalars, defined_on='faces', enabled=True)
    ps.show() 
    '''

    '''
    # Plot all the edges extending out from the current halfedge vertex 
    # Get one ring of vertices, including original vertex 
    vertex_onering = [v.index for v in h.vertex.adjacentVertices()] + [h.vertex.index]
    # Get positions of these vertices 
    onering_positions = mesh.vertices[vertex_onering]
    ps.init()
    # This initializes a mesh object to view in Polyscope 
    ps_mesh = ps.register_surface_mesh("mesh", soup.vertices, soup.indices)
    # Define curve network that connects the vertex to each of its one-ring neighbors 
    curve_edges = np.array([[i, len(onering_positions)-1] for i in range(len(onering_positions)-1)])
    ps_curve = ps.register_curve_network("onering", onering_positions, curve_edges, enabled=True, color=[1,0,0])
    ps.show()
    '''
    
    # Exports current mesh vertices, faces, and edges 
    # TODO: This will only work once you've completed Q1 and Q2 i.e. implemented topology.build() and completed the primitive classes!!! 
    vertices, faces, edges = mesh.export_soup()
    
    # Save current mesh to an obj  
    # TODO: This will only work once you've completed Q1 and Q2 i.e. implemented topology.build() and completed the primitive classes!!! 
    mesh.export_obj("spot_edge_flipped.obj")