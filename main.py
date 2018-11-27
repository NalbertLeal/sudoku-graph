if '__main__' == __name__:
  import multiprocessing as mp
  import numpy as np
  import pandas as pd
  import gc

  # modules of this project
  import color_algorithms.backtrack
  import color_algorithms.greed
  import color_algorithms.ldo
  import color_algorithms.sdo

  # turn off garbage collector to extract maximum performance
  gc.disable()
  gc.set_threshold(0)

  # read the dataset
  sudoku_dataset = pd.read_csv('sudoku_500.csv')

  #  Before start the process we need to create 4 Queue.
  # This Queue going to receive the output from each 
  # process and then we going to work with this results.

  backtrack_queue = mp.Queue()
  greed_queue = mp.Queue()
  ldo_queue = mp.Queue()
  sdo_queue = mp.Queue()

  # Creating the process to run the tests in parallel

  backtrack_process = mp.Process(target=color_algorithms.backtrack.main, args=(backtrack_queue, sudoku_dataset))
  greed_process = mp.Process(target=color_algorithms.greed.main, args=(greed_queue, sudoku_dataset))
  ldo_process = mp.Process(target=color_algorithms.ldo.main, args=(ldo_queue, sudoku_dataset))
  sdo_process = mp.Process(target=color_algorithms.sdo.main, args=(sdo_queue, sudoku_dataset))

  # Start the process to start the tests in parallel

  backtrack_process.start()
  greed_process.start()
  ldo_process.start()
  sdo_process.start()

  #  Wait all the results from the process. Just remenber
  # That the 4 Queue must receive 100 outputs. So below
  # you going to see 4 list compresions that are creating
  # a list with 100 elements.

  backtrack_result = [backtrack_queue.get() for o in range(0, 100)]
  greed_result = [greed_queue.get() for o in range(0, 100)]
  ldo_result = [ldo_queue.get() for o in range(0, 100)]
  sdo_result = [sdo_queue.get() for o in range(0, 100)]

  backtrack_process.join()
  greed_process.join()
  ldo_process.join()
  sdo_process.join()

  #  After that we need to write this results to a Dataset
  # and then make the pd.Dataset write a ".csv" file

  print(backtrack_result)