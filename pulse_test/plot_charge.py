import numpy as np
import matplotlib.pyplot as plt
import colors as cs
import pandas as pd
import scopeplot as scplt
import sys
import os
import time
from scipy.interpolate import spline

folder = sys.argv[-1]


# grabbing filenames from directory
filenames = sorted(os.listdir(folder))
filenames = [f for f in filenames if f.endswith('.csv')]
filenames = filenames[::2]
files = [sys.argv[-1] + f for f in filenames]

# setting up labels for plots
labels = [i[8:-4] for i in filenames]
labels_title = 'waveforms'
lbl_float = [int(i) for i in labels]

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

for key in dataset:
  time_col = dataset[key]['time'][::20]
  channel_col = dataset[key]['chgv'][::20]
  #smoothed = spline(dataset[key]['time'], dataset[key]['chgv'],time)
  dataset[key]['chgv'] = channel_col
  dataset[key]['time'] = time_col

#print dataset
#for d, dset in enumerate(dataset):
#  print d, dset
#  print dset, max(dataset[dset]['chgv']), max(dataset[dset]['loadv'])
#sys.exit()

fig, ax, lines = scplt.plot_mTrace(
    dataset, 
    channel='chgv', 
    time_scale=t_scale,
    channel_scale=chgv_scale, 
    labels=labels, 
    center=True,
    colors=cs.clist(130))
#legend.get_frame().set_alpha(.5)


#   LEGEND PARAMS
legend = ax.legend(fontsize=11, 
  bbox_to_anchor=(1,1),
  ncol=2)
legend.get_frame().set_alpha(.5)

#   PLOT LAYOUT
for line in lines:
  line.set_linewidth(1)
  line.set_alpha(.8)
ax.set_title('EHT RCC Waveforms')
ax.set_xlabel('Time (ns)')
ax.set_ylabel('Voltage (V)')
ax.set_ylim((-1,6))
ax.set_xlim((-500,100))
fig.tight_layout()

fig.savefig(folder + 'Charge_wave_' + str(time.time()) + '.png', transparent=False)
