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


def ResSpec(Ag,dt,Damping,Maxperiod,plot=True):

	gravity = 9.81;

	u  = 0*Ag;
	v  = 0*Ag;
	ac = 0*Ag;

	LengthAg = len(Ag);

	NumSteps = int(Maxperiod/dt+1);
	T = np.linspace(0, Maxperiod, num=NumSteps); # Time Period
	Sd = 0*T;                                    # Spectral Acceleration
	Sv = 0*T;                                    # Spectral Displacement
	Sa = 0*T;                                    # Spectral Acceleration


	for j in range(1,NumSteps):
		omega = 2.0*math.pi/T[j];
		m     = 1.0;                      # mass
		k     = omega*omega*m;            # stiffness
		c     = 2.0*m*omega*Damping/100.0 # viscous damping
		K     = k+3.0*c/dt+6.0*m/(dt**2);
		a     = 6.0*m/dt+3.0*c;
		b     = 3.0*m+dt*c/2.0;

		# initial conditions 
		ac = 0*Ag;
		u  = 0*Ag;
		v  = 0*Ag;

		for i in range(0,LengthAg-1):
			df=-(Ag[i+1]-Ag[i])+a*v[i]+b*ac[i];  # delta Force
			du=df/K;
			dv=3.0*du/dt-3.0*v[i]-dt*ac[i]/2.0;
			dac=6.0*(du-dt*v[i])/(dt)**2.0-3.0*ac[i];
			u[i+1]=u[i]+du;
			v[i+1]=v[i]+dv;
			ac[i+1]=ac[i]+dac; 

		Sd[j]=np.amax( np.absolute(u));
		Sv[j]=np.amax( np.absolute(v));
		Sa[j]=np.amax( np.absolute(ac));

	Sa[0]=np.amax( np.absolute(Ag));

	if(plot):
		fig, ax = plt.subplots()
		ax.plot(T, Sa/gravity,'-k')
		plt.ylabel('Pseudo Response Acceleration (PSa) [g]')
		plt.xlabel('Time Period (T) [s]')
		plt.show()
