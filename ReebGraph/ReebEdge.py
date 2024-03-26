# RG Library Includes
from ReebNode import ReebNode
from MeshEdge import MeshEdge

# Another name for ReebArc (CPP Version)
class ReebEdge:
  def __init__(self, _start : int, _end : int, mesh_edge_index : list[int] = None):
    # Store nodes indices that edge connects (starting and ending)
    self.start : int = _start
    self.end : int = _end

    self.faces : list[int] = [] # Faces associated with this Reeb Edge
    
    # Related Mesh Edges
    self.edges : list[int] = []
    if mesh_edge_index !=  None: # Add initialized mesh edge if it is given
      if type(mesh_edge_index) == int:
        self.edges.append(mesh_edge_index)
      else:
        self.edges.extend(mesh_edge_index)

  # Return starting node
  def get_start(self) -> int:
    return self.start
  
  # Return ending node
  def get_end(self) -> int:
    return self.end
  
  # Returns mesh edge indices
  def get_mesh_edge_indices(self) -> list[int]:
    return self.edges
  
  # Checks equality by comparing start and ending Reeb Nodes
  def __eq__(self, other):
    return other.start == self.start and other.end == self.end

  # To string for Reeb Edges that returns the start and end indices
  def __str__(self) -> str:
    return "(RE: " + str(self.start) + " " +  str(self.end) + " " + str(self.edges) + ")"
  