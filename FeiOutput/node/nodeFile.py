#!/usr/bin/env python

"""Module to return the feioutput File for a given node tag
and upon failure it would return None.
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

def nodeFile(file,tag):
	""" return the filename where the node tag data is 
	stored. On failure it returns None. """

	if(tag<0):
		MainHDF5File = None;
		print "ERROR:: ESSI Node tag " + str(tag) +" does not exist\n";
		return MainHDF5File;

	HDF5_File               = h5py.File(file, 'r');
	ProcessId               = HDF5_File['Process_Number'][0];
	NumProcess              = HDF5_File['Number_of_Processes_Used'][0];

	MainHDF5File            = file;

	if(NumProcess>1):
		if(ProcessId==0):
			PartitionId      = HDF5_File['Model/Nodes/Partition'][tag];
			if(PartitionId>0):
				MainHDF5File = MainHDF5File.split('.feioutput')[0]+'.'+str(PartitionId)+'.feioutput';
			else:
				MainHDF5File = None;

	if(MainHDF5File is None):
		print "ERROR:: ESSI Node tag " + str(tag) +" does not exist\n";
		return MainHDF5File;

	HDF5_File               = h5py.File(MainHDF5File, 'r');
	NumDofs                 = HDF5_File['Model/Nodes/Number_of_DOFs'][tag];

	if(NumDofs==-1):
		MainHDF5File = None;
		print "ERROR:: ESSI Node tag " + str(tag) +" does not exist\n";
		return MainHDF5File;

	return MainHDF5File





