import numpy as np
import pandas as pd

def avg_pwr(filename):
  data = pd.read_csv(filename, sep='\t', header=2).values
  return np.average(data[:,2].astype(np.float32))
