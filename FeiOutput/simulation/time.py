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
import sys,cStringIO;
from simulation import *

class time:
	'It represents an REAL-ESSI Time'

	numSteps              = -1;
	time                  = -1;
	file                  = None;
	__HDF5_File           = None;

	def __str__(self):
		return "\
\n---------------------------------------\n\
ESSI Simulation Time Steps ->\n---------------------------------------\n\t\
Number of Steps :: %s\n\t\
Time :: %s\n\t\
" % (self.NumSteps,self.Time)

	def __init__ (self,file):
		""" Define ESSItime class with output file

		Class Variables:
		file   -- HDF5 output file 
		"""

		self.file = file;
		self.__initialize();


	def __initialize(self):
		""" Initializes the variables by getting data from 
		HDF5 output file
		"""
		self.__HDF5_File        = h5py.File(self.file, 'r');
		self.Time               = (self.__HDF5_File['time'][:]).astype(float);
		self.NumSteps           = len(self.Time);



SequentialFeioutputFilename = './Input_Files/NPPModel_Self_Weight_Check_Model.h5.feioutput';
ParallelFeioutputFileName   = './Input_Files/NPPModel_Self_Weight.h5.feioutput';

X = time(ParallelFeioutputFileName);
print X;


