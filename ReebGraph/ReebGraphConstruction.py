class ReebGraph:
  def __init__(self, vertices, triangles):
    # RG members
    self.reeb_edges = []
    self.reeb_nodes = []

    # Sort vertices by morse function
    sorted_vertex_indices = MorseFunction.sort_vertices(vertices)
    sorted_triangles_vertices = MorseFunction.sort_triangles(sorted_vertex_indices, triangles)


    # Initialize graph
    # Create vertices
    reeb_edges = []
    for counter, vertex in enumerate(vertices):
      reeb_edges.append(ReebNode(counter))

    # Order triangle vertices first


    # Create edges
    for triangle in triangles:
      self.reeb_nodes.append(ReebEdge(triangle[0], triangle[1]))
      self.reeb_nodes.append(ReebEdge(triangle[1], triangle[2]))
      self.reeb_nodes.append(ReebEdge(triangle[0], triangle[2]))

      # Sort vertices
      # Sort vertices within triangles
    # Construct Graph stuff
    # embed graph
    
class MorseFunction:
  # Sorts vertices
  def sort_vertices(vertices):
    # Sort indices of vertices by x positions
    sorted_indices = sorted(range(len(vertices)), key=lambda i: vertices[i][0])
    return sorted_indices
  
  # Sorts triangle vertices based on their positions in the sorted_vertex_indices array
  def sort_triangles(sorted_vertex_indices, triangles):
    sorted_triangles = []
    for triangle in triangles:
      # Sort the indices of the first three vertices based on their order in sorted_vertex_indices
      sorted_indices = sorted(range(3), key=lambda i: sorted_vertex_indices.index(triangle[i]))
      # Rearrange the triangle vertices based on the sorted indices
      sorted_triangles.append((triangle[sorted_indices[0]], triangle[sorted_indices[1]], triangle[sorted_indices[2]]))

    return sorted_triangles
      

  
class ReebNode:
  def __init__(self, index):
    self.index = index

class ReebEdge:
  def __init__(self, first_index, second_index):
    # Edge data
    self.edge_data = None 

    # Nodes indicies that edge connects
    self.node1 = first_index
    self.node2 = second_index