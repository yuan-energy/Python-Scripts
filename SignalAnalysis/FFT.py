#!/usr/bin/env python

"""Contains Fuction for signal analysis
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
import math

def FFT(x,dt,maxf,plot=True):

	# Number of samplepoints
	N = x.size;
	# Total Time 
	T = N*dt;
	# sample dpacing is dt
	# sampling frequency
	Fs = 1/dt;
	xfft  = scipy.fftpack.fft(x);
	xfreq = np.linspace(0.0, Fs/2, N/2);

	xfftHalf = 2.0/N * np.abs(xfft[:N//2]);
	xfftHalf[0] = xfftHalf[0]/2;

	if(plot):
		fig, ax = plt.subplots()
		ax.plot(xfreq, xfftHalf,'-k')
		if(maxf is not None):
			plt.xlim(0, maxf)
		plt.ylabel('Fourier transform |FFT(x)|')
		plt.xlabel('Frequency |Hz|')
		plt.show()

	return xfreq, xfftHalf
