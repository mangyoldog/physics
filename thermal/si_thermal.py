import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import ticker
import sys
import time
import colors

osr = 0.1
pulsewidth = 10e-9

# fixed quantities
Z = 3.96 #Ohms
Vlt = np.linspace(1e2,1e4,100)
Cur = np.linspace(10,5e3, 100)
dT = 50
recovery_factor = 1
rf = recovery_factor

cols = [(1,0,0), (0,1,0), (0,0,1)]
lines = ['--', '-', ':']

#plot heat
plt.figure(figsize=(5,4))
plt.subplots_adjust(right=.6)
for i, s in enumerate([5, 34]):
  sarea = 2.
  rf = s
  print s
  for j, x in enumerate([.5,1,1.5,3, 5]):
    freq = x*1e5
    heat = (Vlt/2/(osr+Z))**2*osr*pulsewidth*freq
    trans_coef = np.log10(heat/dT/sarea*rf)
    plt.plot(Vlt, trans_coef, label='%.0f-kHz' % (freq/1e3), \
         color=colors.clist()[j], linestyle=lines[i+1], linewidth=2)
plt.xlabel('Charge Voltage $(V)$', fontsize=12) 
plt.ylabel('log(H) (W/cm$^2$K)', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.ylim((-4,3))
legend = plt.legend(loc='best', fontsize=10, ncol=2)
legend.get_frame().set_alpha(0.6)
plt.tight_layout()
plt.savefig('Heat_Flux_V_%s.png' % time.time(), transparent=True)
plt.close()
plt.figure(figsize=(5,4))
plt.subplots_adjust(right=.6)
for i, s in enumerate([5, 34]):
  sarea = 2.
  rf = s
  print s
  for j, x in enumerate([.5,1,1.5,3, 5]):
    freq = x*1e5
    heat = (Cur)**2*osr*pulsewidth*freq
    trans_coef = np.log10(heat/dT/sarea*rf)
    plt.plot(Cur, trans_coef, label='%.0f-kHz' % (freq/1e3), \
         color=colors.clist()[j], linestyle=lines[i+1], linewidth=2)
plt.xlabel('Charge Current $(A)$', fontsize=12) 
plt.ylabel('log(H) (W/cm$^2$K)', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
legend = plt.legend(loc='best', fontsize=10, ncol=2)
legend.get_frame().set_alpha(0.6)
plt.ylim((-4,3))
plt.tight_layout()
plt.savefig('Heat_Flux_I_%s.png' % time.time(), transparent=True)
plt.close()
