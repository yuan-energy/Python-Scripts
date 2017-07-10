#!/usr/bin/env python

"""Module to return the absolute or relative output
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

def eleOutpt(file,tag,index=None):
	""" gets the ESSI element output for
	a given element tag
	"""

	# get the element file 
	ElementFile                  = eleFile(file,tag);

	# return None if element file is not correct
	if (ElementFile is None):
		return None;

	HDF5_File          = h5py.File(ElementFile, 'r');
	IndexToOutput      = HDF5_File['Model/Elements/Index_to_Element_Outputs'][tag];
	ClassTag           = HDF5_File['Model/Elements/Class_Tags'][tag];
	ClassTagDesc       = ELE_TAG_DESC_ARRAY[ClassTag];
	NumElementOutput   = NUMBER_OF_ELEMENT_OUTPUTS(ClassTagDesc);

	if (index is not None):
		DispData = np.transpose(HDF5_File['Model/Elements/Element_Outputs'][IndexToOutput:IndexToOutput+NumElementOutput])[index];
	else:
		DispData = np.transpose(HDF5_File['Model/Elements/Element_Outputs'][IndexToOutput:IndexToOutput+NumElementOutput])[:];

	return DispData.astype(float)


def eleRelOutpt(file,tag,relIndex=0,index=None):
	""" gets the relative ESSI element output for
	a given element tag
	"""

	# get the element file 
	ElementFile                  = eleFile(file,tag);

	# return None if element file is not correct
	if (ElementFile is None):
		return None;

	HDF5_File          = h5py.File(ElementFile, 'r');
	IndexToOutput      = HDF5_File['Model/Elements/Index_to_Element_Outputs'][tag];
	ClassTag           = HDF5_File['Model/Elements/Class_Tags'][tag];
	ClassTagDesc       = ELE_TAG_DESC_ARRAY[ClassTag];
	NumElementOutput   = NUMBER_OF_ELEMENT_OUTPUTS(ClassTagDesc);

	if (index is not None):
		DispData = np.transpose(HDF5_File['Model/Elements/Element_Outputs'][IndexToOutput:IndexToOutput+NumElementOutput])[index] -  np.transpose(HDF5_File['Model/Elements/Element_Outputs'][IndexToOutput:IndexToOutput+NumElementOutput])[relindex];
	else:
		DispData = np.transpose(HDF5_File['Model/Elements/Element_Outputs'][IndexToOutput:IndexToOutput+NumElementOutput])[:];

		NumSteps = DispData.shape[0];

		disp = np.empty([NumElementOutput,])

		for i in range(0,NumElementOutput):
			disp[i] = DispData[relIndex][i];

		for i in range(0,NumSteps):
			for j in range(0,NumElementOutput):
				DispData[i][j]=DispData[i][j]- disp[j];		

	return DispData.astype(float)

