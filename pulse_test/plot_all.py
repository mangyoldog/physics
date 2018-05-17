import numpy as np
import matplotlib.pyplot as plt
import colors as cs
import pandas as pd
import scopeplot as scplt
import sys
import os
import time

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
#sys.exit()

#barfig = scplt.plot_osrs_bars(dataset, 
#    loadv_scale=1000, color=(1,0,0),
#    use_lbl_as_x=True, width=.2)
#barfig.savefig('./fig.png')
lbl_float = [i[0:2] for i in labels]
alt_x = [float(lab) for lab in lbl_float]
scattery = scplt.plot_osrs_scatter(dataset,
    loadv_scale=1., color='k', alt_x=alt_x)
scattery.axes[0].set_title('Minimum On-state Resistance')
scattery.axes[0].set_xlabel(labels_title)
scattery.axes[0].set_ylabel('Resistance (Ohms)')
scattery.tight_layout()
#plt.tight_layout()
#plt.show()
scattery.savefig('osr.png', transparent=True)

lines = scplt.plot_osrs_dt(dataset, loadv_scale=1., time_scale=t_scale,
    labels=labels, center=True)
lines.axes[0].set_xlabel('Time (ns)')
lines.axes[0].set_ylabel('Resistance (Ohms)')
lines.axes[0].set_xlim((-10,20))
lines.axes[0].set_ylim((-2,6))
legend = lines.axes[0].legend(fontsize=9)
lines.axes[0].set_title('Time-dependant On-state Resistance')
for line in legend.get_lines():
  line.set_linewidth(2)
lines.tight_layout()
lines.savefig('osr_dtv_' + str(time.time()) + '.png', transparent=True)

lines = scplt.plot_mCH_dt(dataset, channel='chgv', time_scale=t_scale,
    channel_scale=1, labels=labels, center=True)
legend.get_frame().set_alpha(.5)
#   PLOT PARAMS
lines.axes[0].set_title('EHT RCC Waveforms')
lines.axes[0].set_xlabel('Time (ns)')
lines.axes[0].set_ylabel('Voltage (V)')
lines.axes[0].set_ylim((0,600))
#lines.axes[0].set_xlim((-10,20))
#lines.axes[0].set_xlim((-200,200))
#   LEGEND PARAMS
legend = lines.axes[0].legend(fontsize=11, bbox_to_anchor=(1,1),
    ncol=2)
for line in legend.get_lines():
  line.set_linewidth(2)
for line in lines.axes[0].get_lines():
  line.set_alpha(.6)
legend.get_frame().set_alpha(.5)
lines.tight_layout()
lines.savefig('chargevv_' + str(time.time()) + '.png', transparent=True)

lines = scplt.plot_mCH_dt(dataset, channel='loadv', time_scale=t_scale,
    channel_scale=1., labels=labels, center=True)
#   PLOT PARAMS
lines.axes[0].set_xlabel('Time (ns)')
lines.axes[0].set_ylabel('Voltage (V)')
#lines.axes[0].set_xlim((-10,20))
lines.axes[0].set_ylim((0,400))
#   LEGEND PARAMS
legend = lines.axes[0].legend(fontsize=11, bbox_to_anchor=(1,1),
    ncol=1)
lines.axes[0].set_title('Load Waveforms')
for line in legend.get_lines():
  line.set_linewidth(2)
for line in lines.axes[0].get_lines():
  line.set_alpha(.8)
legend.get_frame().set_alpha(.5)
lines.tight_layout()
lines.savefig('loadev_' + str(time.time()) + '.png', transparent=True)

for i, lbl in enumerate(labels):
  lines = scplt.plot_chgload_dt(dataset[lbl], loadv_scale=1, 
      chgv_scale=1., center=True, figsize=(5,4), time_scale=t_scale)
  # PLOT PARAMS
  #lines.axes[0].set_title('1.36uJ Waveforms')
  lines.axes[0].set_xlabel('Time (ns)')
  lines.axes[0].set_ylabel('Load Voltage (V)')
  lines.axes[1].set_ylabel('Charge Voltage (V)')
  lines.axes[0].set_title(lbl)
  #lines.axes[0].set_xlim((-5,15))
  lines.axes[0].set_ylim((0,600))
  lines.axes[1].set_ylim((0,600))
  l1 = lines.axes[0].get_lines()[0]
  l2 = lines.axes[1].get_lines()[0]
  legend.get_frame().set_alpha(.5)
  for line in lines.axes[0].get_lines():
    line.set_alpha(.8)
    line.set_linewidth(2)
  for line in lines.axes[1].get_lines():
    line.set_alpha(.6)
    line.set_linewidth(2)
  #    LEGEND PARAMS
  #legend = plt.figlegend((l2,l1),('ChargeV', 'LoadV'), (.72,.77), fontsize=12)
  #l1, l2, fontsize=10, bbox_to_anchor=(.9,.8))
  lines.tight_layout()
  lines.savefig('chgloadevv' + '_%s_' % lbl + '_%s' % str(time.time()) + '.png', transparent=True)

