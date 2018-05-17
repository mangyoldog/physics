import numpy as np
import matplotlib.pyplot as plt
import sys

def heatingpower(resistance, current):
    return resistance * current**2 #power

def temprise(heatcap, heat):
    return heat/heatcap #dT

def contactdrop(thermresist, heatflowrate):
    return thermresist*heatflowrate #dT

def heatcap(specific, mass):
    return specific*mass #heatcap

def calc_avgpwr(prf, pwidth, pcurrent, OSR):
    return prf*pwidth*(pcurrent**2) * OSR


def printhelp():
    print ''
    print 'heatingpower(resistance, current):'
    print 'temprise(heatcap, heat):'
    print 'contactdrop(thermresist, heatflowrate):'
    print 'heatcap(specific, mass):'
    print 'calc_avgpwr(prf, pwidth, pcurrent, OSR):'
    print 'calc_avgpwr(prf, pwidth, pcurrent, OSR):'
