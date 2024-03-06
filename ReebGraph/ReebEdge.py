# RG Library Includes
from ReebNode import ReebNode
from MeshEdge import MeshEdge


class ReebEdge:
  def __init__(self, first_index : int, second_index : int, mesh_edge : MeshEdge = None):
    # Edge data
    self.edge_data : list[ReebEdge] = [] 

    # Related Mesh Edges
    self.edges : list[MeshEdge] = []
    if mesh_edge !=  None: # Add initialized mesh edge if it is given
      self.edges.append(mesh_edge)


    # Store nodes indices that edge connects
    self.start = first_index
    self.end = second_index

  # Return starting node
  def get_start(self) -> ReebNode:
    return self.start
  
  # Return ending node
  def get_end(self) -> ReebNode:
    return self.end
  
  # Checks equality by comparing start and ending Reeb Nodes
  def __eq__(self, other):
    return other.start == self.start and other.end == self.end

  def __str__(self) -> str:
    return str(self.start) + " " +  str(self.end) + " " + str(self.merged)
  