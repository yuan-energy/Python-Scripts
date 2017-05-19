#!/usr/bin/env python

"""Base class for Real ESSI

It can read input and output of Real ESSI Simulator System
and can perform various task.
"""


import h5py;
import sys,cStringIO
import ESSIoutput;
import ESSIinput;

class RealESSI:
	'It is the class for Real ESSI Simulator System \
	which contains all the modules '

	FeiOutputFile = None;
	FeiInputFile  = None;

	def __str__(self):
		return "\
\n---------------------------------------\n\
REAL ESSI Simulator System \n---------------------------------------\n\t\
FeiInputFile :: %s\n\t\
FeiOutputFile:: %s\n\t\
" % (self.FeiInputFile,self.FeiOutputFile)

	def __init__ (self,outputFile,inputFile=None):
		""" Define ESSI_Output class with output file

		Class Variables:
		FeiOutputFile   -- the hdf5.feioutput filename
		FeiInputFile   -- the .fei input file
		"""
		self.FeiOutputFile = outputFile;
		self.FeInputFile   = inputFile;

	def Output(self):
		""" returns the feioutput file object"""
		return ESSI_Output(self.FeiOutputFile);

	def Input(Self):
		""" returns the feiinput file object"""
		return ESSI_Input(self.FeiInputFile);
		
  

# filename = 'Beam_Axial_Load.h5.feioutput';
# X = RealESSI(filename);
# print X
# time = [1,2]
# T = X.TimeDisp(0);
# print X;
# print T;
# print X.TimeDisp(0);