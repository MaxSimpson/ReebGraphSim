class ReebNode:
  def __init__(self, index : int, order : int):
    self.index = index
    self.order = order

  def __str__(self) -> str:
    return str(self.index)