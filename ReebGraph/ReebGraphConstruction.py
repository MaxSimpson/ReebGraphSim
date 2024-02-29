# OpenGL includes
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from ReebNode import ReebNode
from ReebEdge import ReebEdge

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
    # RG members
    self.reeb_edges: list[ReebEdge] = []
    self.reeb_nodes: list[ReebNode] = []
    self.vertices = vertices # Required to do rendering later

    # Sort vertices by morse function
    sorted_vertex_indices = MorseFunction.sort_vertices(vertices)
    # Order triangle vertices first
    sorted_triangles_vertices = MorseFunction.sort_triangles(sorted_vertex_indices, triangles)

    # Initialize graph
    # Create vertices
    for counter, vertex in enumerate(vertices):
      self.reeb_nodes.append(ReebNode(counter))

    # Create edges
    for triangle in sorted_triangles_vertices:
      self.reeb_edges.append(ReebEdge(triangle[0], triangle[1]))
      self.reeb_edges.append(ReebEdge(triangle[1], triangle[2]))
      self.reeb_edges.append(ReebEdge(triangle[0], triangle[2]))

    # Merge longest edge of every triangle
    counter = 0
    for triangle in sorted_triangles_vertices:
      print("merging ", self.reeb_edges[counter])
      self.reeb_edges[counter].merge(self.reeb_edges[counter + 2])
      self.reeb_edges[counter + 1].merge(self.reeb_edges[counter + 2])

      counter += 3


    print(sorted_triangles_vertices)
    for obj in self.reeb_edges:
      print(obj, " ", end="")

    # Construct Graph stuff
    # embed graph
      
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

