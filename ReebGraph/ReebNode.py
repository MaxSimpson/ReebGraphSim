# Reeb node class
# Each reeb node composes a reeb edge.
# All nodes have an order value assigned by the morse function
class ReebNode:
  def __init__(self, index : int, order : int):
    self.index = index # Specific Index of this Reeb Node
    self.order = order # Ordered value of this Reeb Node

  def __str__(self) -> str:
    return str(self.index)