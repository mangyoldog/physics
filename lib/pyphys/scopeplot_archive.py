import numpy as np
import matplotlib.pyplot as plt
import colors as cs
import pandas as pd

colors = cs.clist()

def del_nonfloat(filename, delim=',', header=None):
  """ reads file and removes all lines after header which do not contain
  float-like strings then overwrites the file after adding the header back in"""
  filein = open(filename, 'r')
  lines = ''
  deleted = 0
  if header is None:
    rlines = filein.readlines()
  else:
    rlines = filein.readlines()[header:]
  filein.close()
  for l in rlines:
    words = l.rstrip('/n').split(delim)
    try:
      [float(w) for w in words]
      lines += l
    except:
      deleted += 1
  fileout = open(filename, 'w')
  fileout.write(lines)
  fileout.close()
  return deleted

def clp_dataset_fmcsv(filenames, chgCH, loadCH, photoCH, header=None, labels=None, v=False):
  """ Returns a time/chgv/loadv/photod dataset of data collected from the filenames provided
  Note: will return error if there are non-float values in the file after header
   ---> use del_nonfloat first"""
  dataset = {}
  for i, f in enumerate(filenames):
    fromcsv = pd.read_csv(f, sep=',', \
        header=header, dtype=np.float32).values
    if v:
      print fromcsv[:,0]
      print fromcsv[:,1]
      print fromcsv[:,2]
      print fromcsv[:,3]
    #fromcsv = fromcsv[np.dtype is np.str]
    data = {}
    data['time'] = fromcsv[:,0]
    data['chgv'] = fromcsv[:,chgCH]
    data['loadv']= fromcsv[:,loadCH]
    data['photo']= fromcsv[:,photoCH]
    if labels is None:
      dataset['%s' % f.split('/')[-1][:-4]] = data
    else:
      if v:
        print dataset
        print labels[i]
        print i
      dataset[labels[i]] = data
  return dataset

def plot_osrs_bars(dataset, loadR=3.9, use_lbl_as_x=False, 
    time_scale=1., chgv_scale=1., loadv_scale=.1, color=(0,0,0), width=None):
  """ Returns a barplot figure of osrs in the order of the dataset provided.
  requres time/chgv/loadv dataset """
  labels = [data for data in dataset]
  if use_lbl_as_x:
    barsx = [float(lbl) for lbl in labels]
  else:
    barsx = np.arange(len(dataset))
  minosrs = []
  fig = plt.figure(figsize=(5,4))
  Plot = fig.add_subplot(111)
  for i, data in sorted(enumerate(dataset)):
    chgv = dataset[data]['chgv'] * chgv_scale
    loadv = dataset[data]['loadv'] * loadv_scale
    minosrs.append((max(chgv)/2-max(loadv))/loadR)
  if width is None:
    Plot.bar(barsx, minosrs, align='center', color=color)
  else:
    Plot.bar(barsx, minosrs, width, align='center', color=color)
  Plot.set_title('On-state Resistance')
  Plot.set_xticks(barsx, labels)
  fig.tight_layout()
  return fig
  
def plot_osrs_scatter(dataset, loadR=3.9, time_scale=1., alt_x=None,
    chgv_scale=1., loadv_scale=.1, color=cs.clist()[0]):
  """ Returns a scatterplot figure of osrs in the order of the dataset provided.
  requres time/chgv/loadv dataset """
  fig = plt.figure(figsize=(5,4))
  Plot = fig.add_subplot(111)
  mykeys = sorted(dataset.keys())
  for i, data in enumerate(mykeys):
    minosr = []
    chgv = dataset[data]['chgv'] * chgv_scale
    loadv = dataset[data]['loadv'] * loadv_scale
    minosr = (max(chgv)/2-max(loadv))*loadR/max(loadv)
    if alt_x is None:
      Plot.scatter(i, minosrs[i], color=color)
    else:
      Plot.scatter(alt_x[i], minosr, color=color)
    del chgv, loadv
  Plot.set_title('On-state Resistance')
  fig.tight_layout()
  return fig


#I beleive this is broken, I need to revisit this code with the new scope saving mechanism
def plot_osrs_dt(dataset, time_scale=1., chgv_scale=1., loadv_scale=.1, 
    alpha=0.8, colors=cs.clist(), loadR=3.9, labels=None, center=False):
  """ Returns a lineplot figure of osrs in the order of the dataset provided.
  requres time/chgv/loadv dataset. Note time does not currently work but 
  time scale can be used to adjust the time bins"""
  fig = plt.figure(figsize=(5,4))
  Plot = fig.add_subplot(111)
  mykeys = sorted(dataset.keys())
  for i, data in enumerate(mykeys):
    osr = []
    time = dataset[data]['time'] * time_scale
    maxt = max(time)
    chgv = dataset[data]['chgv'] * chgv_scale
    loadv = dataset[data]['loadv'] * loadv_scale
    #osr = (max(chgv)/2-max(loadv))*loadR/loadv
    osr = (max(chgv)/2-(loadv))*loadR/loadv
    #time = np.linspace(0,maxt,len(time))
    time = time-np.mean(time)
    print len(osr), len(time)
    time = time[[osr>0] and [osr<50]]
    osr = osr[[osr>0] and [osr<50]]
    #time = time - np.median(time)
    if labels is None:
      lbl=data
    else:
      lbl=labels[i]
    Plot.plot(time,osr, color=colors[i], label=lbl, alpha=alpha)
  Plot.set_title('On-state Resistance')
  fig.tight_layout()
  return fig

def plot_mCH_dt(dataset, time_scale = 1., channel='loadv', channel_scale=1., 
    alpha=0.8, colors=cs.clist(), labels=None, center=False):
#  """ Returns a lineplot figure of osrs in the order of the dataset provided.
#  requres time/chgv/loadv dataset. Note time does not currently work but 
#  time scale can be used to adjust the time bins"""
  fig = plt.figure(figsize=(5,4))
  Plot = fig.add_subplot(111)
  mykeys = sorted(dataset.keys())
  for i, data in enumerate(mykeys):
    time = dataset[data]['time'] * time_scale
    maxt = max(time)
    chanv = dataset[data][channel] * channel_scale
    #time = np.linspace(0,maxt,len(time),endpoint=True)
    if center:
      time = time - np.median(time)
    if labels is None:
      lbl=data
    else:
      lbl=labels[i]
    Plot.plot(time,chanv, color=colors[i], label=lbl, alpha=alpha)
  Plot.set_title('Channel Voltage')
  fig.tight_layout()
  return fig


def plot_chgload_dt(data, time_scale = 1., loadv_scale=1., chgv_scale=1., 
    alpha=0.8, colors=cs.clist(), center=False, figsize=(5,4)):
#  """ Returns a lineplot figure of osrs in the order of the dataset provided.
#  requres time/chgv/loadv dataset. Note time does not currently work but 
#  time scale can be used to adjust the time bins"""
  fig, ax1 = plt.subplots(figsize=figsize)
  time = data['time'] * time_scale
  maxt = max(time)
  chgv = data['chgv'] * chgv_scale
  loadv = data['loadv'] * loadv_scale
  #time = np.linspace(0,maxt,len(time),endpoint=True)
  if center:
    time = time - np.median(time)
  ax1.plot(time,loadv, color=colors[0], label='Load', alpha=alpha)
  ax2 = ax1.twinx()
  ax2.plot(time,chgv, color=colors[1], label='Charge', alpha=alpha)
  ax1.set_title('Charge/Load Pulses')
  fig.tight_layout()
  return fig

#f2parse = sys.argv[1:]
#timestamp = dt.datetime.fromtimestamp(time.time()).strftime('%y%m%d-%H%M%S')
#for i, x in enumerate(f2parse):
#  data = pd.read_csv(x, sep=',', header=None, dtype=np.float32).values
#  halflen = len(data)/2
#  t = [j/750.*10 for j in xrange(len(data))]
#  a = data[:,1]*1e3
#  b = data[:,2]/5
#  c = data[:,3]*50
#  print np.shape(t)
#  print np.shape(a)
#  plt.figure(figsize=(6,4))
#  plt.plot(t, a, color=colors[0], alpha=.5, label='LoadV_1x')
#  plt.plot(t, b, color=colors[1], alpha=.5, label='ChargeV_1/5x')
#  plt.plot(t, c, color=colors[2], alpha=.5, label='PhotodiodeV_50x')
#  plt.legend(fontsize=10)
#  plt.title(x.split('/')[-1][:-4])
#  plt.xlim((200,230))
#  plt.tight_layout()
#  plt.savefig('foc_' + x.split('/')[-1][:-4] + '_all.png')
#  plt.close()
#
#
#f2parse = sys.argv[1:]
#timestamp = dt.datetime.fromtimestamp(time.time()).strftime('%y%m%d-%H%M%S')
#colors = [(1,0,0), (0,1,0), (0,0,1), (1,0,1), (0,0,0)]
#for i, x in enumerate(f2parse):
#  data = pd.read_csv(x, sep=',', header=None, dtype=np.float32).values
#  halflen = len(data)/2
#  data = data[:halflen+50000]
#  t = xrange(len(data))
#  a = data[:,1]*1e3
#  b = data[:,2]/5
#  c = data[:,3]*50
#  print np.shape(t)
#  print np.shape(a)
#  plt.figure(figsize=(6,4))
#  plt.plot(t, a, color=colors[0], alpha=.5, label='LoadV_1x')
#  plt.plot(t, b, color=colors[1], alpha=.5, label='ChargeV_1/5x')
#  plt.plot(t, c, color=colors[2], alpha=.5, label='PhotodiodeV_50x')
#  plt.legend(fontsize=10)
#  plt.title(x.split('/')[-1][:-4])
#  plt.savefig(x.split('/')[-1][:-4] + '_all.png')
#  plt.tight_layout()
#  plt.close()
