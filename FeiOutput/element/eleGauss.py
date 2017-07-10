#!/usr/bin/env python

"""Module to return the absolute or relative gauss output
 for a given element tag

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
from   eleFile  import *;
from   eleClass import *;

def eleGauss(file,tag,index=None):
	""" gets the ESSI element gauss output for
	a given element tag
	"""

	# get the element file 
	ElementFile                  = eleFile(file,tag);

	# return None if element file is not correct
	if (ElementFile is None):
		return None;

	HDF5_File          = h5py.File(ElementFile, 'r');
	IndexToOutput      = HDF5_File['Model/Elements/Index_to_Gauss_Point_Coordinates'][tag]*18/3;
	ClassTag           = HDF5_File['Model/Elements/Class_Tags'][tag];
	ClassTagDesc       = ELE_TAG_DESC_ARRAY[ClassTag];
	NumGauss           = NUMBER_OF_GAUSS(ClassTagDesc);
	NumGaussOutputs    = NumGauss*18; # 6 total strain, 6 plastic strain and 6 stress
	print NumGaussOutputs

	if (index is not None):
		DispData = np.transpose(HDF5_File['Model/Elements/Gauss_Outputs'][IndexToOutput:IndexToOutput+NumGaussOutputs])[index];
	else:
		DispData = np.transpose(HDF5_File['Model/Elements/Gauss_Outputs'][IndexToOutput:IndexToOutput+NumGaussOutputs])[:];

	return DispData.astype(float)


def eleRelGauss(file,tag,relIndex=0,index=None):
	""" gets the relative ESSI element gauss output for
	a given element tag
	"""

	# get the element file 
	ElementFile                  = eleFile(file,tag);

	# return None if element file is not correct
	if (ElementFile is None):
		return None;

	HDF5_File          = h5py.File(ElementFile, 'r');
	IndexToOutput      = HDF5_File['Model/Elements/Index_to_Gauss_Point_Coordinates'][tag]*18/3;
	ClassTag           = HDF5_File['Model/Elements/Class_Tags'][tag];
	ClassTagDesc       = ELE_TAG_DESC_ARRAY[ClassTag];
	NumGauss           = NUMBER_OF_GAUSS(ClassTagDesc);
	NumGaussOutputs    = NumGauss*18; # 6 total strain, 6 plastic strain and 6 stress

	if (index is not None):
		DispData = np.transpose(HDF5_File['Model/Elements/Gauss_Outputs'][IndexToOutput:IndexToOutput+NumGaussOutputs])[index] -  np.transpose(HDF5_File['Model/Elements/Gauss_Outputs'][IndexToOutput:IndexToOutput+NumGaussOutputs])[relindex];
	else:
		DispData = np.transpose(HDF5_File['Model/Elements/Gauss_Outputs'][IndexToOutput:IndexToOutput+NumGaussOutputs])[:];

		NumSteps = DispData.shape[0];

		disp = np.empty([NumGaussOutputs,])

		for i in range(0,NumGaussOutputs):
			disp[i] = DispData[relIndex][i];

		for i in range(0,NumSteps):
			for j in range(0,NumGaussOutputs):
				DispData[i][j]=DispData[i][j]- disp[j];		

	return DispData.astype(float)

