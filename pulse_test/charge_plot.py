import numpy as np
import matplotlib.pyplot as plt
import colors as cs
import pandas as pd
import scopeplot as scplt
import sys
import os
import time
from scipy.interpolate import spline

#General setup
folder = sys.argv[-1]
timestamp = str(int(time.time()))
legends=False
ch_type='chgv'
ch_skip=1
rskip = 20 # only grab every rskip'th row
save_calcs=True

# grabbing filenames from directory
filenames = sorted(os.listdir(folder))
filenames = [f for f in filenames if f.endswith('.csv')]
filenames = filenames[::ch_skip]
files = [sys.argv[-1] + f for f in filenames]

# setting up labels for plots
labels = [i[8:-4] for i in filenames]
labels_title = 'waveforms'
lbl_float = [int(i)*5+10 for i in labels]

#setting up scaling factors
t_scale = 1/1e-9
chgv_scale = 1.e-3
loadv_scale = 1.e-3

#removing blank rows from csv
for f in files:
 scplt.del_nonfloat(f), f

#collecting data
dataset = scplt.clp_dataset_fmcsv( 
    files, 2, 3, 1, labels=labels)

#skip rows
for key in sorted(dataset.keys()):
  time_col = dataset[key]['time'][::rskip]
  channel_col = dataset[key][ch_type][::rskip]
  dataset[key][ch_type] = channel_col
  dataset[key]['time'] = time_col


# save calculations
if save_calcs:
  temp = sys.stdout
  calc_filename = 'calcs_%s.txt' % timestamp
  sys.stdout = open(folder + calc_filename, 'w')
  #sys.stdout() = 'calcs_%s.txt' % timestamp
  for key in sorted(dataset.keys()):
    #for channel in dataset[key]:
      channel = 'chgv'
      Name = '%s_%s' % (key, channel)
      Min = np.min(dataset[key][channel])
      Max = np.max(dataset[key][channel])
      Avg = np.average(dataset[key][channel])
      print '%s\t%.2e\t%.2e\t%.2e' % (Name, Min, Max, Avg)
  sys.stdout.close()
  os.system('unix2dos %s' % (folder + calc_filename))
  sys.stdout = temp

# Plot the data
fig, ax, lines = scplt.plot_mTrace(
    dataset, 
    channel='chgv', 
    time_scale=t_scale,
    channel_scale=chgv_scale, 
    labels=labels, 
    center=False,
    colors=cs.clist(len(dataset)/ch_skip))

#   LEGEND PARAMS
if legends:
  legend = ax.legend(fontsize=11, 
    bbox_to_anchor=(1,1),
    ncol=2)
  legend.get_frame().set_alpha(.5)

#   PLOT LAYOUT
for line in lines:
  line.set_linewidth(0.8)
  line.set_alpha(.6)
for line in lines[-4:]:
  line.set_linewidth(2)
  line.set_alpha(0.8)
ax.set_title('EHT RCC Hipot Test')
ax.set_xlabel('Time (ns)')
ax.set_ylabel('Voltage (kV)')
ax.set_ylim((-1,6))
ax.set_xlim((400,800))
fig.tight_layout()

fig.savefig(folder + 'Charge_wave_' + timestamp + '.png', transparent=False)
