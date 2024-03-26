# OpenGL includes
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time

# RG Library
from ReebNode import ReebNode
from ReebEdge import ReebEdge
from MeshEdge import MeshEdge

import traceback

class MorseFunction:
  # Sorts vertices
  def sort_vertices(vertices : list[tuple]) -> list[tuple]:
    morse_values : list[float] = []
    for v in vertices:
      morse_values.append(v[0] + v[2])


    # Sort indices of vertices by x positions 
    sorted_indices = [x for _, x in sorted(zip(morse_values, [i for i in range(len(morse_values))]))]

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
    self.vertices = vertices # Required for rendering later

    # Reeb Graph members
    self.reeb_edges : list[ReebEdge] = []
    self.reeb_nodes : list[ReebNode] = []

    # Edges of Tetrahedralization
    self.mesh_edges : list[MeshEdge] = []

    # Sort vertices by morse function (RG.CPP 290 - 298)
    self.sorted_vertex_indices : list[int] = MorseFunction.sort_vertices(vertices)

    # self.sorted_vertex_indices = [0, 3, 5, 4, 2, 1]
    print(self.sorted_vertex_indices)
    # exit()

    # Order triangle vertices first (RG.CPP 303 - 311)
    self.sorted_triangles_vertices : list[tuple] = MorseFunction.sort_triangles(self.sorted_vertex_indices, triangles)
    print(self.sorted_triangles_vertices)

    # quit()

    # Initialize graph
    # Create vertices of Reeb Graph (RG.CPP 287 - 288)
    for counter, vertex in enumerate(vertices):
      self.reeb_nodes.append(ReebNode(counter, self.sorted_vertex_indices.index(counter)))
      # self.reeb_nodes.append(ReebNode(counter, counter))
    #   print(counter, self.sorted_vertex_indices.index(counter))

    # print(self.sorted_vertex_indices)
    # print(self.vertices)

    # Add each edge to RG as seperate ReebArcs (RG.CPP 314 - 324)
    counter = 0
    for triangle in self.sorted_triangles_vertices:
      self.add_triangle_mesh_edges(triangle, counter)
      counter += 1

    print("Vertices:", self.sorted_vertex_indices)

    # print("\nRE's:")
    # for obj in self.reeb_edges:
    #   print(obj, " ", end="")
    # print()

    # print("\nME's:")
    # for obj in self.mesh_edges:
    #   print(obj, " ", end="")
    # print()

    # Find 3 edges for each triangle and call MergePaths
    for triangle in self.sorted_triangles_vertices:
      print("\nRE's:")
      for obj in self.reeb_edges:
        print(obj, " ", end="")
      print()

      print("\nME's:")
      for obj in self.mesh_edges:
        print(obj, " ", end="")
      print()

      e0 : MeshEdge = next((edge for edge in self.mesh_edges if edge == MeshEdge(triangle[0], triangle[2])), None)
      e1 : MeshEdge = next((edge for edge in self.mesh_edges if edge == MeshEdge(triangle[0], triangle[1])), None)
      e2 : MeshEdge = next((edge for edge in self.mesh_edges if edge == MeshEdge(triangle[1], triangle[2])), None)

      print("Mesh Edges Before\n", e0, e1, e2)
      print("# of Reeb Edges:", len(self.reeb_edges))
      self.merge_paths(e0, e1, e2)

      # Decrement num triangles
      e0.decrement_number_of_triangles()
      e1.decrement_number_of_triangles()
      e2.decrement_number_of_triangles()

      # If edge is done being processed - delete. This is an optimization
      # if e0.number_of_triangles == 0:
      #   self.delete_mesh_edge(e0)
      # if e1.number_of_triangles == 0:
      #   self.delete_mesh_edge(e1)
      # if e2.number_of_triangles == 0:
      #   self.delete_mesh_edge(e2)


    # Remove all 2 node edges from the graph (simplfiying) 
      
    print("\nMesh Edges After")
    for edge in self.mesh_edges:
      print(edge)

    # Debug Outputs
    # print(self.sorted_triangles_vertices)
    print("# of Reeb Edge:", len(self.reeb_edges))
    print("\nReeb Edges:")
    for obj in self.reeb_edges:
      print(obj, " ", end="")
      # print("[",end="")
      # for value in obj.get_mesh_edge_indices():
      #   print(self.mesh_edges[value], " ", end="")
      # print("]",end="\t")
    print()
  
  def merge_paths(self, e0 : MeshEdge, e1 : MeshEdge, e2 : MeshEdge) -> None:
    a0 : list[int] = e0.get_arc_set()
    a1 : list[int] = e1.get_arc_set()
    self.glue_by_merge_sorting(a0, a1)

    a2 : list[int] = e0.get_arc_set()
    a3 : list[int] = e2.get_arc_set()
    self.glue_by_merge_sorting(a2, a3)

  def glue_by_merge_sorting(self, a0 : list[int], a1 : list[int]) -> None:
    # Cycle iterators
    iter0 = iter(a0)
    iter1 = iter(a1)

    asit0 = next(iter0)
    asit1 = next(iter1)

    while True:
      print("asits", self.reeb_edges[asit0], self.reeb_edges[asit1])
      try:

        # Skip the same edges
        if asit0 == asit1:
          asit0 = next(iter0)
          asit1 = next(iter1)
          continue

        # Check if they are valid edges to continue merge
        if self.reeb_edges[asit0].start != self.reeb_edges[asit1].start:
          if self.reeb_arc_comparator(asit0, asit1):
            asit0 = next(iter0)
          else:
            asit1 = next(iter1)
          continue

        n0 : ReebNode = self.reeb_nodes[self.reeb_edges[asit0].get_end()]
        n1 : ReebNode = self.reeb_nodes[self.reeb_edges[asit1].get_end()]

        # Merge based on the order of the target edges
        print("order value:", n0.order, n1.order)
        if n0.order < n1.order:
          self.merge_arcs(asit0, asit1)
          asit0 = next(iter0)

          iter1 = iter(a1)
          asit1 = next(iter1)
        else:
          self.merge_arcs(asit1, asit0)
          asit1 = next(iter1)
          iter0 = iter(a0)
          asit0 = next(iter0)
      except Exception as e: 
        print("EXCEPTION HERE", str(e))
        traceback.print_exc()
        break

  def merge_arcs(self, _a0 : int, _a1 : int):
    a0 : ReebEdge = self.reeb_edges[_a0]
    a1 : ReebEdge = self.reeb_edges[_a1]

    print("merge_arcs before")
    print(a0)
    print(a1)

    # Merge data into a0
    for edge_index in a1.edges:
      print("\tMesh Edge before:", self.mesh_edges[edge_index])
      self.mesh_edges[edge_index].insert(_a0)
      self.mesh_edges[edge_index].erase(_a1)
      a0.edges.append(edge_index)
      print("\tMesh Edge after:", self.mesh_edges[edge_index])
    a0.faces.extend(a1.faces)

    print("merge_arcs after")
    print(a0)
    print(a1)

    # Case: targets are not equal. Insert new edge from a0's target to a1's target
    if a0.end != a1.end:
      print("Targets unequal, adding new edge", a0.end, a1.end)
      self.reeb_edges.append(ReebEdge(a0.end, a1.end, a1.get_mesh_edge_indices()))
      
      for edge_index in self.reeb_edges[-1].get_mesh_edge_indices():
        self.mesh_edges[edge_index].insert(len(self.reeb_edges) - 1)

    # Removing edge so decrease all other reeb edge indices
    print("Deleting:", self.reeb_edges[_a1])
    del self.reeb_edges[_a1]
    for edge in self.mesh_edges:
      edge.adjust_reeb_indices(_a1)

  def reeb_arc_comparator(self, _a : int, _b : int):
    ret : bool = False
    s0 : ReebNode = self.reeb_nodes[self.reeb_edges[_a].get_start()]
    s1 : ReebNode = self.reeb_nodes[self.reeb_edges[_b].get_start()]

    if s0.order < s1.order:
      ret = True
    elif s0.order == s1.order:
      t0 : ReebNode = self.reeb_nodes[self.reeb_edges[_a].get_end()]
      t1 : ReebNode = self.reeb_nodes[self.reeb_edges[_b].get_end()]
      if t0.order < t1.order:
        ret = True
    return ret

  # Create mesh edges in the model based on a triangle and that triangles ID
  def add_triangle_mesh_edges(self, triangle : tuple, triangle_id : int):
    self.create_arc(triangle[0], triangle[2], [triangle_id])
    self.create_arc(triangle[0], triangle[1], [triangle_id])
    self.create_arc(triangle[1], triangle[2], [triangle_id])

  def create_arc(self, start_index : int, end_index : int, faces : list[int] = []) -> MeshEdge:
    # New edge to try and add to graph
    new_edge = MeshEdge(start_index, end_index) 

    # If edge does not exist add an edge in both triangle edges set and reeb arc set
    if self.mesh_edges.count(new_edge) == 0:

      # Create new mesh edge if it does not already exist
      self.mesh_edges.append(new_edge) 

      # Create new reeb graph edge to represent this new mesh edge      
      reeb_graph_edge = ReebEdge(start_index, end_index, len(self.mesh_edges) - 1)
      self.reeb_edges.append(reeb_graph_edge)

      # Link mesh edge to newly created RG Edge
      self.mesh_edges[-1].arc_sets.append(len(self.reeb_edges) - 1)

    # Find working edge to associate triangles with edge's reeb arcs (RG.CPP 374-379)
    working_edge : MeshEdge = next((edge for edge in self.mesh_edges if edge == new_edge), None)
    working_edge.increment_number_of_triangles()
    for edge_index in working_edge.get_arc_set():
      self.reeb_edges[edge_index].faces.extend(faces)

    return working_edge

  # Optimization function has not been implemented yet
  # def delete_mesh_edge(self, edge): 
  #   index : int =  next((find for find in self.mesh_edges if find == edge), None)

      
  # Draw Reeb Edges and Nodes
  def render(self):
    
    # Set line width
    glLineWidth(50.0)

    # Enable line smoothing
    glEnable(GL_LINE_SMOOTH)
    glColor3f(0.0, 1.0, 0.0)  # Set color to green

    # print(self.reeb_edges)
    # for edge in self.reeb_edges:
    #   print(edge.faces)
    # print("\n\n")

    glBegin(GL_LINES)
    for edge in self.reeb_edges:
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

 