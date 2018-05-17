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
numz=20
numx=50
z = np.linspace(0,1e-3,numz)
x= np.linspace(0,1e-2,numx)
dx=x[1]-x[0] # switch width in m
mean = 5e-3
#std = 5e-3
std = float(sys.argv[-1])
intensity_dist = 1/(2*np.pi*std**2)**.5*np.exp(-((x-mean)**2/(2*std**2)))
t_recomb = 1e-6

d = z[1] - z[0] # layer thickness
carrier_peak = []
intensity = [1]

carrier_totals = np.zeros((np.size(x),np.size(z)))
for ii, j in enumerate(x):
  intensity=intensity_dist[ii]
  for i, k in enumerate(z): 
    intensity = intensity*np.exp(-Abs*d)
    #constant factor to include switch volume and light efficiency
    K = (1-R)/(dx*l*d)/(h*c/lmbda)*(intensity)
    #print K, R, dx, l, d, h, c, lmbda, intensity
    R = 0
    #carrier concetration in m^-3 
    n = n0+K*np.exp(-t/t_recomb)*integ.cumtrapz(
        np.exp(t/t_recomb)*Plaser, x=t, initial=0) 
    lab = '%.2f-us' % (t_recomb*1e6)
    logt = np.log10(t)
    carrier_totals[ii,i] = np.max(integ.cumtrapz(n,x=t))
    #if i % (len(z)/10) == 0:
    #  print 'Intensity(x=%.2fmm) =\t%.2e' % (k*1e3, intensity)


plt.imshow(carrier_totals.T, aspect=(z[-1]/x[-1]))
xnum=numx/5
xticklab = ['%d' % (i*1e3) for i in x[::xnum]]
xticks = [i*xnum for i in xrange(len(x[::xnum]))]
znum=numz/2
zticklab = ['%.1f' % (i*1e3) for i in z[::znum]]
zticks = [i*znum for i in xrange(len(z[::znum]))]
plt.xticks(xticks,xticklab)
plt.yticks(zticks,zticklab)
plt.ylabel('%02dmm' % (std*1e3))
plt.savefig(folder + '%02d.png' % (std*1e3), transparent=True)
#plt.show()
