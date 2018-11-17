if '__main__' == __name__:
  import multiprocessing as mp
  import numpy as np
  import pandas as pd  

  from Graph import Graph 
  import tests

  # create the queue that receive the output from the tests
  greed_output = mp.Queue()
  ldo_output = mp.Queue()
  sdo_output = mp.Queue()

  # before any test we need to read the dataset
  # the line of code below read the sudoku dataset
  sudoku_dataset = pd.read_csv('sudoku')

  # Helper functions (function to write less code)

  def tests_loop(function_to_run):
    """
      This function receive by parameter the function test to run test
    inside the loop the repeat 500 times (because we expect each algorithm
    to run 500 times).
    """
    for index in range(0, 500):
      sudoku_dataset.iloc[index] # get the row with the graph input
                                 # and expected output
      graph = Graph() # Create the graph with the input
      function_to_run(greed_output, graph) # start the test

  # Create a function to each algorithm that going to be tested

  def greed_tests(greed_output):
    """
      This function start the test of the greed algorithm. 
    """
    tests_loop(tests.test_greed)

  def ldo_tests(ldo_output):
    """
      This function start the test of the ldo algorithm. 
    """
    tests_loop(tests.test_ldo)

  def sdo_tests(sdo_output):
    """
      This function start the test of the sdo algorithm. 
    """
    tests_loop(tests.test_sdo)

  # create the 3 tests process
  greed_test_proces = smp.Process(target=greed_tests, args=(greed_output))
  ldo_test_process = mp.Process(target=ldo_tests, args=(ldo_output))
  sdo_test_process = mp.Process(target=sdo_tests, args=(sdo_output))

  # start the 3 tests to run at the same time
  greed_test_process.start()
  ldo_test_process.start()
  sdo_test_process.start()

  # wait all the responses to stop the process
  while True:
    if len(greed_output) == 500:
      if len(ldo_output) == 500 and len(sdo_output) == 500:
        #   if all the tests responses as received then stop the 
        # 3 main tests process
        greed_test_process.join()
        ldo_test_process.join()
        sdo_test_process.join()
