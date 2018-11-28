import multiprocessing as mp
import numpy as np
from graph import Graph
from tests.test_sdo import test_sdo

def main(sdo_queue, sudoku_dataset):
  """
    This function have the logic to create the 
  tests of the colouring greed algorithm.
  """
  number_of_next_row = 0
  tests_finished = mp.Queue()
  tests_running = mp.Queue()
  process_list = []
  while tests_finished.qsize() < len(sudoku_dataset): # While don't exists 100 test finished run more tests
    if tests_running.qsize() < 20: # Must have 10 tests running at the same time
      tests_running.put(True) # Another test going to be initiated, so increment the count variable
      sudoku_input_str = str(sudoku_dataset.iat[number_of_next_row,0]) # The sudoku row with the actual input
      number_of_next_row += 1
      sudoku_input_list = list(sudoku_input_str) # The graph receive a list with the sudoku input
      graph = Graph(sudoku_input_list) # Create the graph
      process = mp.Process(target=test_sdo, args=(sdo_queue, graph, tests_finished, tests_running))
      process.start() # start the test
  for p in process_list:
    p.join()