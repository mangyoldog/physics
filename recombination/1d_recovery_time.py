import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate as integ
import colors as cs
import sys
import time

folder = '../../data/recombination/'

#constants
h = 6.62e-34
c = 3.e8

#laser params
t_laser = 70e-12 # laser pulse duration
E_laser=1e-5 # laser energy per pulse in J
lmbda=1064e-9 # laser wavelength in m

#switch params
n0=0 # free carriers concentration is m^-3
w=1e-2 # switch width in m
l=1e-2 # switch length in m
#d=1e-3 #switch thickness in m
R=0 #intensity reflection coeeficient at surface 
Abs=1000 # absorption coefficient at illumination wavelength in m^-1
mu=1400 # electron mobility in cm2/V/s

# build laser pulse in time
#t = np.linspace(-10*t_laser,10*t_laser,1e5)
t = np.linspace(1e-9,2e-4,1e5) # time scale range
t_peak = 1e-9 # laser peak time in seconds
Plaser = np.exp(-4.*np.log(2.)*((t-t_peak)/t_laser)**2.) # Gaussian pulse shape intensity
NRJ = np.max(integ.cumtrapz(Plaser, x=t)) # calculate integral of Plaser over time = energy per pulse
print 'Energy per pulse: %s\nPeak energy: %s' % (E_laser, NRJ)
#sys.exit()
Plaser = Plaser * E_laser/NRJ #normalize laser power function for energy per pulse
#check1_Elaser=np.max(integ.cumtrapz(t,Plaser)) # check elaser is correct
#print check1_Elaser

z = np.linspace(0,5e-3,100)
t_recomb = 1e-6

d = z[1] - z[0] # layer thickness
carrier_peak = []
intensity = [1]
for i, k in enumerate(z): 
  intensity.append(intensity[-1]*np.exp(-Abs*d))
  #constant factor to include switch volume and light efficiency
  K = (1-R)/(w*l*d)/(h*c/lmbda)*(intensity[-1])
  R = 0
  #carrier concetration in m^-3 
  n = n0+K*np.exp(-t/t_recomb)*integ.cumtrapz(
      np.exp(t/t_recomb)*Plaser, x=t, initial=0) 
  lab = '%.2f-us' % (t_recomb*1e6)
  logt = np.log10(t)
  carrier_peak.append(np.max(n))
  if i % (len(z)/10) == 0:
    print 'Intensity(x=%.2fmm) =\t%.2e' % (k*1e3, intensity[-1])
fig, ax1 = plt.subplots()
ax1.plot(z*1e3, carrier_peak, c=cs.clist()[1], lw=2)
ax2 = ax1.twinx()
ax2.plot(z*1e3, intensity[:-1], c=cs.clist()[2], lw=2)
ax1.set_xlabel('Depth (mm)')
ax1.set_ylabel('Carrier Density (#/cm3)')
ax2.set_ylabel('Relative Intensity (AU)')
ax1.set_title('Peak Carrier Density Profile')
ax1col = cs.clist()[1]
ax2col = cs.clist()[2]
ax1.yaxis.label.set_color(ax1col)
ax1.spines['left'].set_color(ax1col)
ax2.spines['left'].set_color(ax1col)
ax1.tick_params(axis='y', colors=ax1col)
ax2.yaxis.label.set_color(ax2col)
ax1.spines['right'].set_color(ax2col)
ax2.spines['right'].set_color(ax2col)
ax2.tick_params(axis='y', colors=ax2col)
ax1.ticklabel_format(style='sci')
ax2.ticklabel_format(style='sci')
plt.savefig(folder + 'carrier_density_%s.png' % str(time.time())[:-3])
plt.show()
plt.close()
