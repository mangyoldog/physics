import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate as integ
import colors as cs
import sys

#constants
h = 6.62e-34
c = 3.e8

#laser params
t_laser = 70e-12 # laser pulse duration
E_laser=1e-6 # laser energy per pulse in J
lmbda=1064e-9 # laser wavelength in m

#switch params
n0=0 # free carriers concentration is m^-3
w=1e-2 # switch width in m
l=1e-2 # switch length in m
d=1e-3 #switch thickness in m
R=0 #intensity reflection coeeficient at surface 
Abs=1000 # absorption coefficient at illumination wavelength in m^-1

# build laser pulse in time
#t = np.linspace(-10*t_laser,10*t_laser,1e5)
t = np.linspace(1e-9,2e-4,1e6) # time scale range
t_peak = 1e-9 # laser peak time in seconds
Plaser = np.exp(-4.*np.log(2.)*((t-t_peak)/t_laser)**2.) # Gaussian pulse shape intensity
NRJ = np.max(integ.cumtrapz(Plaser, x=t)) # calculate integral of Plaser over time = energy per pulse
print NRJ, E_laser
#sys.exit()
Plaser = Plaser * E_laser/NRJ #normalize laser power function for energy per pulse
#check1_Elaser=np.max(integ.cumtrapz(t,Plaser)) # check elaser is correct
#print check1_Elaser

t_recomb_logarray = np.linspace(-4,-7,10) # array of 10^-4 to 10^-7 recombination times, arraysize=10
fig, ax1 = plt.subplots()
for i, logt_recomb in enumerate(t_recomb_logarray): #loop through recombination times in seconds
  t_recomb = 10**logt_recomb  #calculate carrier concnetration as a function of time based on Nunally (eq8)
  K = (1-R)/(w*l*d)/(h*c/lmbda)*(1-np.exp(-Abs*d)) #constant factor to include switch volume and light efficiency
  n = n0+K*np.exp(-t/t_recomb)*integ.cumtrapz(np.exp(t/t_recomb)*Plaser, x=t, initial=0) #carrier concetration in m^-3 
  lab = '%.2f-us' % (t_recomb*1e6)
  logt = np.log10(t)
  ax1.plot(logt, n, label=lab, color=cs.clist()[i])
  #ax2 = ax1.twinx()
  #ax2.plot(t, Plaser, linestyle='--')
plt.xlabel('Log10(Time) (s)')
ax1.set_ylabel('Carrier Density (#/cm3)')
#ax2.set_ylabel('Laser Intensity')
legend = ax1.legend()
#legend.get_frame().set_facecolor('none')
legend.get_frame().set_alpha(0.6)
[i.set_lw(2.) for i in legend.get_lines()]
plt.show()
