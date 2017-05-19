#!/usr/bin/env python

"""Base class for defining node

It contains the information about node of 
Real ESSI Simulator System
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

class ESSI_Node:
	'It represents an REAL-ESSI Node'

	Tag                   = -1;
	Coordinates           = -1;
	NumDofs               = -1;
	ProcessId             = -1;
	__Time                = None;
	IndexToOutput         = -1;
	FeiOutputFile         = None;
	__HDF5_File           = None;
	DofType               = None;

	def __str__(self):
		return "\
\n---------------------------------------\n\
ESSI Node Number -> %s\n---------------------------------------\n\t\
Coordinates:: %s\n\t\
NumDofs:: %s\n\t\
DofType:: %s\n\t\
IndexToOutput:: %s\n\t\
ProcessId:: %s\n\t\
FeiOutputFile:: %s\n\t\
" % (self.Tag,self.Coordinates,self.NumDofs,self.DofType,self.IndexToOutput,\
	self.ProcessId,self.FeiOutputFile)

	def __init__ (self,Tag,FeiOutputFile):
		""" Define ESSI_Node class with output file

		Class Variables:
		Tag -- REAL ESSI Node stag
		FeiOutputFile   -- HDF5 output file 
		"""

		self.Tag           = Tag;
		self.FeiOutputFile = FeiOutputFile;
		self.__initialize();


	def __initialize(self):
		""" Initializes the variables by getting data from 
		HDF5 output file
		"""
		self.__HDF5_File        = h5py.File(self.FeiOutputFile, 'r');
		Index_to_Coordinates    = self.__HDF5_File['Model/Nodes/Index_to_Coordinates'][self.Tag];
		self.Coordinates        = self.__HDF5_File['Model/Nodes/Coordinates'][Index_to_Coordinates:Index_to_Coordinates+3];
		self.IndexToOutput      = self.__HDF5_File['Model/Nodes/Index_to_Generalized_Displacements'][self.Tag];
		self.NumDofs            = self.__HDF5_File['Model/Nodes/Number_of_DOFs'][self.Tag];
		self.ProcessId          = self.__HDF5_File['Process_Number'][0];

		if (self.NumDofs==3):
			self.DofType, DofInfo = self.__DispInfo3DOF();
		elif (self.NumDofs==4):
			self.DofType, DofInfo = self.__DispInfo4DOF();
		elif (self.NumDofs==6):
			self.DofType, DofInfo = self.__DispInfo6DOF();
		elif (self.NumDofs==7):
			self.DofType, DofInfo = self.__DispInfo7DOF();

	def TimeStepDisp(self, TimeStep):
		""" gets the ESSI Node output at a 
		given TimeStep 
		"""
		return self.__HDF5_File['Model/Nodes/Generalized_Displacements'][self.IndexToOutput:self.IndexToOutput+self.NumDofs][:,TimeStep:TimeStep+1];

	def TimeDisp(self, Time):
		""" gets the ESSI Node output at a 
		given Time
		"""

		TimeStep1, TimeStep2 = self.__FindTimeStep(Time);

		if(TimeStep1==-1 and TimeStep2 == -1):
			return -1;

		TimeList           = self.__HDF5_File['time'][:];

		DispData = None;
		if(TimeStep2==0):
			DispData = self.__HDF5_File['Model/Nodes/Generalized_Displacements'][self.IndexToOutput:self.IndexToOutput+self.NumDofs][:,TimeStep2:TimeStep2+1]
		else:
			TimeStep1Data = self.__HDF5_File['Model/Nodes/Generalized_Displacements'][self.IndexToOutput:self.IndexToOutput+self.NumDofs][:,TimeStep1:TimeStep1+1]
			TimeStep2Data = self.__HDF5_File['Model/Nodes/Generalized_Displacements'][self.IndexToOutput:self.IndexToOutput+self.NumDofs][:,TimeStep2:TimeStep2+1]
			Time1 = TimeList[TimeStep1];
			Time2 = TimeList[TimeStep2];

			DispData = TimeStep1Data + (TimeStep2Data - TimeStep1Data)/(Time2-Time1)*(Time-Time1); 

		return DispData;

	def Disp(self,index):
		""" gets the ESSI Node output at a 
		given Time Index List
		"""

		DispData = np.transpose(np.transpose(self.__HDF5_File['Model/Nodes/Generalized_Displacements'][self.IndexToOutput:self.IndexToOutput+self.NumDofs])[index]);

		return DispData

	def __FindTimeStep(self, Time):
		""" find the TimeSteps [TimeStep1,TimeStep2] for 
		the given Time 
		"""
		TimeList           = self.__HDF5_File['time'][:];
		NumSteps           = len(TimeList);

		TimeStep1 = -1;
		TimeStep2 = -1;

		if(Time >=TimeList[0]):
			for i in range(0,NumSteps):
				if(TimeList[i]>=Time):
					TimeStep2 = i;
					TimeStep1 = i-1;
					break;

		if(TimeStep1==-1 and TimeStep2 == -1):
			print "ERROR:: TimeDisp  could not find data for the specified time " + str(Time);
			return -1,-1;

		return TimeStep1,TimeStep2


	def DispInfo(self):
		""" shows the output data documentation """

		DofType = None;
		DofInfo = None;

		if (self.NumDofs==3):
			DofType, DofInfo = self.__DispInfo3DOF();
		elif (self.NumDofs==4):
			DofType, DofInfo = self.__DispInfo4DOF();
		elif (self.NumDofs==6):
			DofType, DofInfo = self.__DispInfo6DOF();
		elif (self.NumDofs==7):
			DofType, DofInfo = self.__DispInfo7DOF();

		DofPrint = "\n---------------------------------------\n";
		DofPrint = DofPrint + "Disp Info Node Number -> "+ str(self.Tag) +"\n---------------------------------------\n\t";

		index = 0;
		for index in xrange(0,len(DofType)):
			DofPrint = DofPrint + "["+str(index)+"] :: "+ DofType[index] + "  " +  DofInfo[index] + "\n\t";

		# print the information 
		print DofPrint


	def __DispInfo3DOF(self):
		DofType = ["ux","uy","uz"];
		DofInfo = ["Displacement in x-direction", "Displacement in y-direction", "Displacement in z-direction" ];
		return DofType, DofInfo;

	def __DispInfo4DOF(self):
		DofType = ["ux","uy","uz","p"];
		DofInfo = ["Displacement in x-direction", "Displacement in y-direction", "Displacement in z-direction",\
		"Pressure" ];
		return DofType, DofInfo;

	def __DispInfo6DOF(self):
		DofType = ["ux","uy","uz","rx","ry","rz"];
		DofInfo = ["Displacement in x-direction", "Displacement in y-direction", "Displacement in z-direction",\
		"Rotation about x-axis", "Rotation about y-axis", "Rotation about z-axis" ];
		return DofType, DofInfo;

	def __DispInfo7DOF(self):
		DofType = ["ux","uy","uz","p","Ux","Uy","Uz"];
		DofInfo = ["Solid Displacement in x-direction", "Solid Displacement in y-direction", "Solid Displacement in z-direction",\
		"Pore Pressure", "Fluid Displacement in x-direction", "Fluid Displacement in z-direction", "Fluid Displacement in z-direction" ];
		return DofType, DofInfo;	



###### Example ###########################
# filename = 'Beam_Axial_Load.h5.feioutput';
# X = ESSI_Node(2,filename);
# time = [1,2]
# T = X.TimeDisp(0);
# print X;
# print T;
# print X.TimeDisp(0);

