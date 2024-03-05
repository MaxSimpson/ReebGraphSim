class MeshEdge:
  def __init__(self, start_index : int, end_index : int):
    self.start = start_index  # Source vertex index
    self.end = end_index      # Target vertex index
    self.number_of_triangles: int = 1   # Number of triangles in mesh edge
    self.arc_sets: list[tuple] = []

  def get_start(self) -> int:
    return self.start
  
  def get_end(self) -> int:
    return self.end
  