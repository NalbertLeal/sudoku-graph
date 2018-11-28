if '__main__' == __name__:
  import multiprocessing as mp
  import numpy as np
  import pandas as pd
  import gc

  #  Modules of this project that handle the test in a parallel way
  import parallel_handler.backtrack
  import parallel_handler.greed
  import parallel_handler.ldo
  import parallel_handler.sdo

  import util.list_utils

  #  Turn off garbage collector to extract maximum performance
  gc.disable()
  gc.set_threshold(0)

  #  Read the dataset
  sudoku_dataset = pd.read_csv('sudoku_medium.csv')

  #  Before start the process we need to create 4 Queue.
  # This Queue going to receive the output from each 
  # process and then we going to work with this results.

  backtrack_queue = mp.Queue()
  greed_queue = mp.Queue()
  ldo_queue = mp.Queue()
  sdo_queue = mp.Queue()

  #  Creating the process to run the tests in parallel

  backtrack_process = mp.Process(target=parallel_handler.backtrack.main, args=(backtrack_queue, sudoku_dataset))
  greed_process = mp.Process(target=parallel_handler.greed.main, args=(greed_queue, sudoku_dataset))
  ldo_process = mp.Process(target=parallel_handler.ldo.main, args=(ldo_queue, sudoku_dataset))
  sdo_process = mp.Process(target=parallel_handler.sdo.main, args=(sdo_queue, sudoku_dataset))

  #  Start the process to start the tests in parallel

  backtrack_process.start()
  greed_process.start()
  ldo_process.start()
  sdo_process.start()

  #  Wait all the results from the process. Just remenber
  # that the 4 Queue must receive 100 outputs. So below
  # you going to see 4 list compresions that are creating
  # a list with 100 elements.

  backtrack_result = [backtrack_queue.get() for o in range(0, len(sudoku_dataset))]
  greed_result = [greed_queue.get() for o in range(0, len(sudoku_dataset))]
  ldo_result = [ldo_queue.get() for o in range(0, len(sudoku_dataset))]
  sdo_result = [sdo_queue.get() for o in range(0, len(sudoku_dataset))]

  #  Close the process

  backtrack_process.join()
  greed_process.join()
  ldo_process.join()
  sdo_process.join()

  #  We need to clean the results

  backtrack_correct = []
  backtrack_answer = []
  backtrack_time = []
  for result in backtrack_result:
    if type(result[1]) == type('str'):
      # result is an error
      backtrack_correct.append(False)
      backtrack_answer.append(result[1])
      backtrack_time.append(result[0])
    else:
      # result is the sudoku answer
      string_of_result =  util.list_utils.list_to_str(result[1]) # convert the list of the result to string 
      backtrack_correct.append(True)
      backtrack_answer.append(string_of_result)
      backtrack_time.append(result[0])

  greed_correct = []
  greed_answer = []
  greed_time = []
  for result in greed_result:
    if type(result[1]) == type('str'):
      # result is an error
      greed_correct.append(False)
      greed_answer.append(''.join(result[1]))
      greed_time.append(result[0])
    else:
      # result is the sudoku answer
      string_of_result = util.list_utils.list_to_str(result[1]) # convert the list of the result to string 
      greed_correct.append(True)
      greed_answer.append(string_of_result)
      greed_time.append(result[0])

  ldo_correct = []
  ldo_answer = []
  ldo_time = []
  for result in ldo_result:
    if type(result[1]) == type('str'):
      # result is an error
      ldo_correct.append(False)
      ldo_answer.append(result[1])
      ldo_time.append(result[0])
    else:
      # result is the sudoku answer
      string_of_result = util.list_utils.list_to_str(result[1]) # convert the list of the result to string 
      ldo_correct.append(True)
      ldo_answer.append(string_of_result)
      ldo_time.append(result[0])

  sdo_correct = []
  sdo_answer = []
  sdo_time = []
  for result in sdo_result:
    if type(result[1]) == type('str'):
      # result is an error
      sdo_correct.append(False)
      sdo_answer.append(result[1])
      sdo_time.append(result[0])
    else:
      # result is the sudoku answer
      string_of_result = util.list_utils.list_to_str(result[1]) # convert the list of the result to string 
      sdo_correct.append(True)
      sdo_answer.append(string_of_result)
      sdo_time.append(result[0])

  #  Create a list with the rows of each dataset result

  backtrack_clean = [pd.Series(backtrack_correct, name='correct'), pd.Series(backtrack_answer, name='answer'), pd.Series(backtrack_time, name='time')]  
  greed_clean = [pd.Series(greed_correct, name='correct'), pd.Series(greed_answer, name='answer'), pd.Series(greed_time, name='time')]
  ldo_clean = [pd.Series(ldo_correct, name='correct'), pd.Series(ldo_answer, name='answer'), pd.Series(ldo_time, name='time')]
  sdo_clean = [pd.Series(sdo_correct, name='correct'), pd.Series(sdo_answer, name='answer'), pd.Series(sdo_time, name='time')]

  #  After that we need to write this results to a Dataset

  backtrack_dataset = pd.concat(backtrack_clean, axis=1, keys=[s.name for s in backtrack_clean])
  greed_dataset = pd.concat(greed_clean, axis=1, keys=[s.name for s in greed_clean])
  ldo_dataset = pd.concat(ldo_clean, axis=1, keys=[s.name for s in ldo_clean])
  sdo_dataset = pd.concat(sdo_clean, axis=1, keys=[s.name for s in sdo_clean])

  
  # Write the pd.Dataset to a ".csv" file

  backtrack_dataset.to_csv('backtrack_dataset', sep=';')
  greed_dataset.to_csv('greed_dataset', sep=';')
  ldo_dataset.to_csv('ldo_dataset', sep=';')
  sdo_dataset.to_csv('sdo_dataset', sep=';')