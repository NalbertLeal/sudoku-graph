import numpy as np
import pandas as pd 
import time

def test_greed(output, graph):
  start = time.time()
  graph.greed()
  end = time.time()
  output.put(end - start)

def test_greed(output, graph):
  start = time.time()
  graph.ldo()
  end = time.time()
  output.put(end - start)

def test_greed(output, graph):
  start = time.time()
  graph.sdo()
  end = time.time()
  output.put(end - start)