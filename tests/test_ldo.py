import time

def test_ldo(ldo_queue, graph, tests_finished, tests_runnig):
  result = [] # This test return this list
  start = time.time()

  algorithm_output = None
  try:
    algorithm_output = graph.ldo()
  except Exception as e:
    algorithm_output = e

  end = time.time()

  result.append(end - start) # The first element of the list is the time
  result.append(algorithm_output) # The second element of the list is the algorithm output

  ldo_queue.put(result) # Put the result in the queue
  
  tests_finished.put(True) # Inform that another test is over
  tests_runnig.get() # Inform that can run another test, because this test is done