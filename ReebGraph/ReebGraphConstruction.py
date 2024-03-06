# OpenGL includes
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from ReebNode import ReebNode
from ReebEdge import ReebEdge
from MeshEdge import MeshEdge

class MorseFunction:
  # Sorts vertices
  def sort_vertices(vertices : list[tuple]) -> list[tuple]:
    # Sort indices of vertices by x positions
    sorted_indices = sorted(range(len(vertices)), key=lambda i: vertices[i][0])
    return sorted_indices
  
  # Sorts triangle vertices based on their positions in the sorted_vertex_indices array
  def sort_triangles(sorted_vertex_indices : list, triangles : list[tuple]) -> list[tuple]:
    sorted_triangles : list[tuple] = []
    for triangle in triangles:
      # Sort the indices of the first three vertices based on their order in sorted_vertex_indices
      sorted_indices = sorted(range(3), key=lambda i: sorted_vertex_indices.index(triangle[i]))

      # Rearrange the triangle vertices based on the sorted indices
      sorted_triangles.append((triangle[sorted_indices[0]], triangle[sorted_indices[1]], triangle[sorted_indices[2]]))

    return sorted_triangles

class ReebGraph:

  def __init__(self, vertices : list[tuple], triangles : list[tuple]):
    # Reeb Graph members
    self.reeb_edges : list[ReebEdge] = []
    self.reeb_nodes : list[ReebNode] = []
    self.vertices = vertices # Required for rendering later

    # Edges of Tetrahedralization
    self.edges : list[MeshEdge] = []

    # Sort vertices by morse function (RG.CPP 290 - 298)
    sorted_vertex_indices = MorseFunction.sort_vertices(vertices)

    # Order triangle vertices first (RG.CPP 303 - 311)
    sorted_triangles_vertices : list[tuple] = MorseFunction.sort_triangles(sorted_vertex_indices, triangles)

    # Initialize graph
    # Create vertices of Reeb Graph (RG.CPP 287 - 288)
    for counter, vertex in enumerate(vertices):
      self.reeb_nodes.append(ReebNode(counter))

    # Add each edge to RG as seperate ReebArcs (RG.CPP 314 - 324)
    counter = 0
    for triangle in sorted_triangles_vertices:
      counter += self.add_triangle_mesh_edges(triangle, counter)

    # Call MergePaths on each triangle

    # Remove all 2 node edges from the graph (simplfiying) 

    print(sorted_triangles_vertices)
    print(self.reeb_edges)
    for obj in self.reeb_edges:
      print(obj, " ", end="")

    # embed graph
  

  # Create mesh edges in the model based on a triangle and that triangles ID
  def add_triangle_mesh_edges(self, triangle : tuple, triangle_id : int) -> int:
    arcs_added = 0 # Counter for the number of new arcs

    # Record how many arcs we actually added (some triangles share mesh edges so ignore)
    arcs_added += self.create_arc(triangle[0], triangle[2], [triangle_id])
    arcs_added += self.create_arc(triangle[0], triangle[1], [triangle_id])
    arcs_added += self.create_arc(triangle[1], triangle[2], [triangle_id])

    # Return the number of new arcs
    return arcs_added


  def create_arc(self, start_index : int, end_index : int, faces : list[int]) -> int:
    new_edge = MeshEdge(start_index, end_index) # New edge to try and add to graph

    # If edge does not exist add an edge in both triangle edges set and reeb arc set
    if self.edges.count(new_edge) == 0:
      new_edge.increment_number_of_triangles()
      self.edges.append(new_edge)
      reeb_graph_edge = ReebEdge(start_index, end_index, )

    # Associate triangles with edge's reeb arcs

      


    return 0

    

  # Add reeb edge to the graph
  def add_reeb_edge(self, new_edge: ReebEdge) -> bool:
    for edge in self.reeb_edges:
      if new_edge == edge: 
        return False # Return because edge already exists 
    self.reeb_edges.append(new_edge)
    print()
      
  # Draw Reeb Edges and Nodes
  def render(self):
    
    # Set line width
    glLineWidth(50.0)

    # Enable line smoothing
    glEnable(GL_LINE_SMOOTH)
    glColor3f(0.0, 1.0, 0.0)  # Set color to green

    glBegin(GL_LINES)
    for edge in self.reeb_edges:
      if edge.merged:
        continue
      # print(self.reeb_edges)
      # Draw lines
      glVertex3f(*self.vertices[edge.get_start()])
      glVertex3f(*self.vertices[edge.get_end()])
    glEnd()

    # Draw Reeb nodes
    glPointSize(15.0)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POINTS)
    counter = 1
    for point in self.reeb_nodes:
      glColor3f(1/counter, 0, 0)
      counter += 1
      glVertex3f(*self.vertices[point.index])
      
    glEnd()

