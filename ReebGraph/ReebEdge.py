from ReebNode import ReebNode

class ReebEdge:
  def __init__(self, first_index : int, second_index : int):
    # Edge data
    self.edge_data : list[ReebEdge] = [] 
    self.merged = False

    # Nodes indicies that edge connects
    self.start = first_index
    self.end = second_index

  def get_start(self) -> ReebNode:
    return self.start
  def get_end(self) -> ReebNode:
    return self.end
  
  def __eq__(self, other):
    return other.start == self.start and other.end == self.end

  def __str__(self) -> str:
    return str(self.start) + " " +  str(self.end) + " " + str(self.merged)
  
  def merge(self, mergedEdge : ReebNode) -> None:
    print("merging edge")
    self.edge_data += mergedEdge.edge_data
    mergedEdge.merged = True