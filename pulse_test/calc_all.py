import numpy as np
import matplotlib.pyplot as plt
import colors as cs
import pandas as pd
import scopeplot as scplt
import sys
import os
import time
import scipy.integrate as integrate

folder = sys.argv[-1]

labels = [
    '20_VDC',
    '25_VDC',
    '30_VDC']

labels_title = 'DC Supply Voltage (V)'

filenames = sorted(os.listdir(folder))
files = [sys.argv[-1] + f for f 
    in filenames if f.endswith('.csv')]

t_scale = 1/1e-9

for f in files:
 scplt.del_nonfloat(f), f

dataset = scplt.clp_dataset_fmcsv(files, 2, 3, 1, labels=labels)

#print dataset

for d, dset in enumerate(dataset):
  print d, dset
  print dset, max(dataset[dset]['chgv']), max(dataset[dset]['loadv'])
  y = dataset[dset]['loadv']
  x = dataset[dset]['time']
  dt = x[1]-x[0]
  print x
  print 'dt is %s' % dt
  #tmiddle = np.median(x)
  #tstart = x[[y==max(y)]]
  print np.average(x), max(x), min(x)
  #print 'middle time is %s' % tmiddle
  #vpulse = y[[x>tmiddle] and [x<(tmiddle + 1e-8)]]
  vpulse = y[4900:5200]
  plt.plot(vpulse)
  plt.show()
  plt.close()
  Vall_integral = integrate.trapz(y, dx=dt)
  print 'total integral is %s' % Vall_integral
  Vpulse_integral = integrate.trapz(vpulse,dx=dt) 
  print 'pulse integral is %s' % Vpulse_integral
  ratio = (Vall_integral-Vpulse_integral)/Vpulse_integral
  print 'ratio is %s' % ratio
#sys.exit()


