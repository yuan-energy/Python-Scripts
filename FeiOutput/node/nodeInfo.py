#!/usr/bin/env python

"""Module to return information about node

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

def nodeInfo(file,tag):
	""" gets the ESSI Node displacement for
	a given node tag
	"""

	# get the node file 
	NodeFile                  = nodeFile(file,tag);

	# return None if nodefile is not correct
	if (NodeFile is None):
		return None;

	HDF5_File               = h5py.File(NodeFile, 'r');
	Index_to_Coordinates    = HDF5_File['Model/Nodes/Index_to_Coordinates'][tag];
	Coordinates             = HDF5_File['Model/Nodes/Coordinates'][Index_to_Coordinates:Index_to_Coordinates+3];
	IndexToOutput           = HDF5_File['Model/Nodes/Index_to_Generalized_Displacements'][tag];
	NumDofs                 = HDF5_File['Model/Nodes/Number_of_DOFs'][tag];
	ProcessId               = HDF5_File['Process_Number'][0];

	if (NumDofs==3):
		DofType, DofInfo = __DispInfo3DOF();
	elif (NumDofs==4):
		DofType, DofInfo = __DispInfo4DOF();
	elif (NumDofs==6):
		DofType, DofInfo = __DispInfo6DOF();
	elif (NumDofs==7):
		DofType, DofInfo = __DispInfo7DOF();

	PrintInfo =  "\
\n---------------------------------------\n\
ESSI Node Number -> %s\n---------------------------------------\n\t\
Coordinates:: %s\n\t\
NumDofs:: %s\n\t\
DofType:: %s\n\t\
DofInfo:: %s\n\t\
IndexToOutput:: %s\n\t\
ProcessId:: %s\n\t\
FeiOutputFile:: %s\n\t\
" % (tag,Coordinates,NumDofs,DofType,DofInfo,IndexToOutput,\
	ProcessId,NodeFile)

	return PrintInfo;

def __DispInfo3DOF():
	DofType = ["ux","uy","uz"];
	DofInfo = ["Displacement in x-direction", "Displacement in y-direction", "Displacement in z-direction" ];
	return DofType, DofInfo;

def __DispInfo4DOF():
	DofType = ["ux","uy","uz","p"];
	DofInfo = ["Displacement in x-direction", "Displacement in y-direction", "Displacement in z-direction",\
	"Pressure" ];
	return DofType, DofInfo;

def __DispInfo6DOF():
	DofType = ["ux","uy","uz","rx","ry","rz"];
	DofInfo = ["Displacement in x-direction", "Displacement in y-direction", "Displacement in z-direction",\
	"Rotation about x-axis", "Rotation about y-axis", "Rotation about z-axis" ];
	return DofType, DofInfo;

def __DispInfo7DOF():
	DofType = ["ux","uy","uz","p","Ux","Uy","Uz"];
	DofInfo = ["Solid Displacement in x-direction", "Solid Displacement in y-direction", "Solid Displacement in z-direction",\
	"Pore Pressure", "Fluid Displacement in x-direction", "Fluid Displacement in z-direction", "Fluid Displacement in z-direction" ];
	return DofType, DofInfo;	
