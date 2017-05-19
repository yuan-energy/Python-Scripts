#!/usr/bin/env python

"""Base class for defining simulation time

It contains the information about simulation time of 
Real ESSI Simulator System Analysis
"""

__author__ = "Sumeet K. Sinha"
__credits__ = [""]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Sumeet K. Sinha"
__email__ = "sumeet.kumar507@gmail.com"


import h5py;
import sys,cStringIO

class ESSI_Time:
	'It represents an REAL-ESSI Time'

	NumSteps              = -1;
	Time                  = -1;
	FeiOutputFile         = None;
	__HDF5_File           = None;

	def __str__(self):
		return "\
\n---------------------------------------\n\
ESSI Simulation Time Steps ->\n---------------------------------------\n\t\
Number of Steps :: %s\n\t\
Time :: %s\n\t\
" % (self.NumSteps,self.Time)

	def __init__ (self,FeiOutputFile):
		""" Define ESSI_Time class with output file

		Class Variables:
		FeiOutputFile   -- HDF5 output file 
		"""

		self.FeiOutputFile = FeiOutputFile;
		self.__initialize();


	def __initialize(self):
		""" Initializes the variables by getting data from 
		HDF5 output file
		"""
		self.__HDF5_File        = h5py.File(self.FeiOutputFile, 'r');
		self.Time               = self.__HDF5_File['time'][:];
		self.NumSteps           = len(self.Time);




# filename = 'Beam_Axial_Load.h5.feioutput';
# X = ESSI_Time(filename);
# print X;

# filename = 'NPPModel_DRM_Motion.h5.feioutput';
# X = FeiOutput(filename);
# print X;


