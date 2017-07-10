#!/usr/bin/env python

"""Returns Simulation time vector
"""

__author__ = "Sumeet K. Sinha"
__credits__ = [""]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Sumeet K. Sinha"
__email__ = "sumeet.kumar507@gmail.com"


import h5py;


def simTime(file,index=None):
	""" gets the ESSI Node acceleration for
	a given node tag
	"""

	HDF5_File          = h5py.File(file, 'r');

	if (index is not None):
		TimeData = HDF5_File['time'][index];
	else:
		TimeData = HDF5_File['time'][:];

	return TimeData.astype(float)

