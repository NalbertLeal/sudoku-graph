import numpy as np
import pandas as pd 
import time

def test_greed(output, graph, tests_finished, tests_runnig):
  result = []
  start = time.time()

  graph.greed()

  end = time.time()
  output.put([end - start, result[0]])
  tests_finished += 1
  tests_runnig -= 1

def test_greed(output, graph, tests_finished, tests_runnig):
  result = []
  start = time.time()

  graph.ldo()
  
  end = time.time()
  output.put([end - start, result[0]])
  tests_finished += 1
  tests_runnig -= 1

def test_greed(output, graph, tests_finished, tests_runnig):
  result = []
  start = time.time()

  graph.sdo(result)
  
  end = time.time()
  output.put([end - start, result[0]])
  tests_finished += 1
  tests_runnig -= 1