class MeshEdge:
  def __init__(self, start_index : int, end_index : int):
    self.start = start_index  # Source vertex index
    self.end = end_index      # Target vertex index
    self.number_of_triangles: int = 1   # Number of triangles in mesh edge
    self.arc_sets: list[tuple] = []

  # Check that the both mesh edges contain the same start and end
  def __eq__(self, other: object) -> bool:
    return other.start == self.start and other.end == self.end
  
  # Return the starting point of mesh edge
  def get_start(self) -> int:
    return self.start
  
  # Return the end of the mesh edge
  def get_end(self) -> int:
    return self.end
  
  # Increment number of triangles
  def increment_number_of_triangles(self) -> None:
    self.number_of_triangles += 1

  # Addes triangles to the current arc set
  def add_triangles(self, new_triangles : list[int]) -> None:
    self.arc_sets.extend(new_triangles)