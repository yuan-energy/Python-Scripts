#!/usr/bin/env python

"""Module to return the absolute or relative displacement for a given node tag

"""

__author__ = "Sumeet K. Sinha"
__credits__ = [""]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Sumeet K. Sinha"
__email__ = "sumeet.kumar507@gmail.com"


import h5py;
import sys,cStringIO;
import numpy as np;
from   nodeFile import *;

def nodeDisp(file,tag,index=None):
	""" gets the ESSI Node displacement for
	a given node tag
	"""

	# get the node file 
	NodeFile                  = nodeFile(file,tag);

	# return None if nodefile is not correct
	if (NodeFile is None):
		return None;

	HDF5_File          = h5py.File(NodeFile, 'r');
	IndexToOutput      = HDF5_File['Model/Nodes/Index_to_Generalized_Displacements'][tag];
	NumDofs            = 3; # ux uy uz

	if (index is not None):
		DispData = np.transpose(HDF5_File['Model/Nodes/Generalized_Displacements'][IndexToOutput:IndexToOutput+NumDofs])[index];
	else:
		DispData = np.transpose(HDF5_File['Model/Nodes/Generalized_Displacements'][IndexToOutput:IndexToOutput+NumDofs])[:];

	return DispData.astype(float)


def nodeRelDisp(file,tag,relIndex=0,index=None):
	""" gets the relative ESSI Node displacement for
	a given node tag
	"""

	# get the node file 
	NodeFile                  = nodeFile(file,tag);

	# return None if nodefile is not correct
	if (NodeFile is None):
		return None;

	HDF5_File          = h5py.File(NodeFile, 'r');
	IndexToOutput      = HDF5_File['Model/Nodes/Index_to_Generalized_Displacements'][tag];
	NumDofs            = 3; # ux uy uz

	if (index is not None):
		DispData = np.transpose(HDF5_File['Model/Nodes/Generalized_Displacements'][IndexToOutput:IndexToOutput+NumDofs])[index] -  np.transpose(HDF5_File['Model/Nodes/Generalized_Displacements'][IndexToOutput:IndexToOutput+NumDofs])[relindex];
	else:
		DispData = np.transpose(HDF5_File['Model/Nodes/Generalized_Displacements'][IndexToOutput:IndexToOutput+NumDofs])[:];

		NumSteps = DispData.shape[0];

		disp = np.empty([NumDofs,])

		for i in range(0,NumDofs):
			disp[i] = DispData[relIndex][i];

		for i in range(0,NumSteps):
			for j in range(0,NumDofs):
				DispData[i][j]=DispData[i][j]- disp[j];		

	return DispData.astype(float)

