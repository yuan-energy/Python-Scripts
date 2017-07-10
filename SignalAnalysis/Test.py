#!/usr/bin/env python

"""This Script as name suggests tests all the functions of the modules

The models considered here are RealESSI, ESSIelement, ESSInode, ESSItime,
ESSIinput, ESSIoutput. The input files for the scripts are present in 
Input_Files directory
"""

__author__ = "Sumeet K. Sinha"
__credits__ = [""]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Sumeet K. Sinha"
__email__ = "sumeet.kumar507@gmail.com"

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from SignalAnalysis import *

# Number of samplepoints
N = 60000
# sample spacing
T = 1.0 / 800
x = np.linspace(0.0, N*T, N)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)

x,y = FFT(y,T,100)
print x
print y 
