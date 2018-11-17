import numpy as np 

class Graph():
  def __init__(self, vertices_list=[]):
    self.vertices = np.array(vertices_list)
    self.edges = np.zeros(shape=(len(self.vertices), len(self.vertices)))

  def get_adjacents(self, vertice_index):
    """
      Using the self.edges return a np.array with the index of the 
    vertices that are adjacent of the "vertice_index" of the paramenter.
    """
    pass

  def greed(self):
    pass

  def ldo(self):
    pass

  def sdo(self):
    pass