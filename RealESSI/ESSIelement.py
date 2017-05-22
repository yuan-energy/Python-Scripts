#!/usr/bin/env python

"""Base class for defining element

It contains the information about elements of 
Real ESSI Simulator System
"""

__author__ = "Sumeet K. Sinha"
__credits__ = [""]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Sumeet K. Sinha"
__email__ = "sumeet.kumar507@gmail.com"


import h5py;
import sys,cStringIO
import ESSIclass
import numpy as np;

class ESSI_Element:
	'It represents an REAL-ESSI element'

	Tag                   = -1;
	Connectivity          = -1;
	MaterialTag           = -1;
	ClassTag              = -1;
	Name                  = "CompGeoMechanicUCDElement";
	ProcessId             = -1;
	ClassTagDesc          = -1;
	__Time                = None;
	IndexToGaussOutput    = None;
	IndexToElementOutput  = None;
	FeiOutputFile         = None;
	GaussPointCoordinates = None;
	NumNodes              =  0;
	NumGauss              =  0;
	NumGaussOutput        =  0;
	NumElementOutput      =  0;
	__HDF5_File			  = None;
	GaussOutputType       = None;
	ElementOutputType     = None;


	def __str__(self):
		return "\
\n---------------------------------------\n\
%s -> %s\n---------------------------------------\n\t\
Connectivity:: %s\n\t\
NumNodes:: %s\n\t\
NumGauss:: %s\n\t\
MaterialTag:: %s\n\t\
NumElementOutput:: %s\n\t\
NumGaussOutput:: %s\n\t\
ElementOutput:: %s\n\t\
GaussOutput:: %s\n\t\
IndexToGaussOutput:: %s\n\t\
IndexToElementOutput:: %s\n\t\
ClassTag:: %s\n\t\
ClassTagDesc:: %s\n\t\
ProcessId:: %s\n\t\
FeiOutputFile:: %s\n\t\
" % (self.Name, self.Tag,self.Connectivity,self.NumNodes,self.NumGauss,\
	self.MaterialTag,self.NumElementOutput,self.NumGaussOutput,self.ElementOutputType,\
	self.GaussOutputType,self.IndexToElementOutput,self.IndexToGaussOutput,\
	self.ClassTag,self.ClassTagDesc,self.ProcessId,self.FeiOutputFile)

	def __init__ (self,Tag,FeiOutputFile):
		""" Define ESSI_Element class with output file

		Class Variables:
		Tag -- REAL ESSI Element stag
		FeiOutputFile   -- HDF5 output file 
		"""

		self.Tag           = Tag;
		self.FeiOutputFile = FeiOutputFile;
		self.__initialize();


	def __initialize(self):
		""" Initializes the variables by getting data from 
		HDF5 output file
		"""
		self.__HDF5_File             = h5py.File(self.FeiOutputFile, 'r');
		Index_to_Connectivity        = self.__HDF5_File['Model/Elements/Index_to_Connectivity'][self.Tag];
		self.IndexToElementOutput    = self.__HDF5_File['Model/Elements/Index_to_Element_Outputs'][self.Tag];
		self.IndexToGaussOutput      = self.__HDF5_File['Model/Elements/Index_to_Gauss_Point_Coordinates'][self.Tag];
		self.ClassTag                = self.__HDF5_File['Model/Elements/Class_Tags'][self.Tag];
		self.ClassTagDesc            = ESSIclass.ELE_TAG_DESC_ARRAY[self.ClassTag];
		self.Name                    = str.strip(ESSIclass.ELE_NAME[self.ClassTag-1]);
		self.MaterialTag             = self.__HDF5_File['Model/Elements/Material_Tags'][self.Tag];
		self.NumNodes                = ESSIclass.NUMBER_OF_NODES(self.ClassTagDesc);
		self.NumGauss                = ESSIclass.NUMBER_OF_GAUSS(self.ClassTagDesc);
		self.NumGaussOutput          = self.NumGauss*18;
		self.NumElementOutput        = ESSIclass.NUMBER_OF_ELEMENT_OUTPUTS(self.ClassTagDesc);
		self.Connectivity            = self.__HDF5_File['Model/Elements/Connectivity'][Index_to_Connectivity:Index_to_Connectivity+self.NumNodes];
		self.ProcessId               = self.__HDF5_File['Process_Number'][0];
		
		self.ElementOutputType, ElementOutputInfo, Status = ESSIclass.ElementOutputInfo(self.ClassTag);
		self.GaussOutputType = ["et_xx","et_yy","et_zz","et_xy","et_yz","et_xz"];
		self.GaussOutputType = self.GaussOutputType + ["ep_xx","ep_yy","ep_zz","ep_xy","ep_yz","ep_xz"];
		self.GaussOutputType = self.GaussOutputType + ["s_xx","s_yy","s_zz","s_xy","s_yz","s_xz"];

		if(self.NumGauss>0):
			self.GaussPointCoordinates   = (self.__HDF5_File['Model/Elements/Gauss_Point_Coordinates'][self.IndexToGaussOutput/18*3:self.IndexToGaussOutput/18*3+3*self.NumGauss]).reshape((3,self.NumGauss));

	def TimeStepElementOutput(self, TimeStep):
		""" gets the ESSI Node output at a 
		given TimeStep 
		"""

		if(self.NumElementOutput<=0):
			return -1;

		return self.__HDF5_File['Model/Elements/Element_Outputs'][self.IndexToElementOutput:self.IndexToElementOutput+self.NumElementOutput][:,TimeStep:TimeStep+1];

	def TimeElementOutput(self, Time):
		""" gets the ESSI Element output at a 
		given Time 
		"""

		if(self.NumElementOutput<=0):
			return -1;

		TimeStep1, TimeStep2 = self.__FindTimeStep(Time);

		if(TimeStep1==-1 and TimeStep2 == -1):
			return -1;

		TimeList           = self.__HDF5_File['time'][:];

		ElementOutput = None;
		if(TimeStep2==0):
			ElementOutput = self.__HDF5_File['Model/Elements/Element_Outputs'][self.IndexToElementOutput:self.IndexToElementOutput+self.NumElementOutput][:,TimeStep2:TimeStep2+1]
		else:
			TimeStep1Data = self.__HDF5_File['Model/Elements/Element_Outputs'][self.IndexToElementOutput:self.IndexToElementOutput+self.NumElementOutput][:,TimeStep1:TimeStep1+1]
			TimeStep2Data = self.__HDF5_File['Model/Elements/Element_Outputs'][self.IndexToElementOutput:self.IndexToElementOutput+self.NumElementOutput][:,TimeStep2:TimeStep2+1]
			Time1 = TimeList[TimeStep1];
			Time2 = TimeList[TimeStep2];

			ElementOutput = TimeStep1Data + (TimeStep2Data - TimeStep1Data)/(Time2-Time1)*(Time-Time1); 

		return ElementOutput;


	def TimeStepGaussOutput(self, TimeStep):
		""" gets the ESSI Node output at a 
		given TimeStep 
		"""
		if(self.NumGaussOutput<=0):
			return -1;
		
		GaussOutput = self.__HDF5_File['Model/Elements/Gauss_Outputs'][self.IndexToGaussOutput:self.IndexToGaussOutput+self.NumGaussOutput][:,TimeStep:TimeStep+1];
		return GaussOutput.reshape((18, self.NumGauss));	

	def TimeGaussOutput(self, Time):
		""" gets the ESSI Gauss output at a 
		given Time 
		"""

		if(self.NumGaussOutput<=0):
			return -1;

		TimeStep1, TimeStep2 = self.__FindTimeStep(Time);

		if(TimeStep1==-1 and TimeStep2 == -1):
			return -1;

		TimeList           = self.__HDF5_File['time'][:];

		GaussOutput = None;
		if(TimeStep2==0):
			GaussOutput = self.__HDF5_File['Model/Elements/Gauss_Outputs'][self.IndexToGaussOutput:self.IndexToGaussOutput+self.NumGaussOutput][:,TimeStep2:TimeStep2+1]
		else:
			TimeStep1Data = self.__HDF5_File['Model/Elements/Gauss_Outputs'][self.IndexToGaussOutput:self.IndexToGaussOutput+self.NumGaussOutput][:,TimeStep1:TimeStep1+1]
			TimeStep2Data = self.__HDF5_File['Model/Elements/Gauss_Outputs'][self.IndexToGaussOutput:self.IndexToGaussOutput+self.NumGaussOutput][:,TimeStep2:TimeStep2+1]
			Time1 = TimeList[TimeStep1];
			Time2 = TimeList[TimeStep2];

			GaussOutput = TimeStep1Data + (TimeStep2Data - TimeStep1Data)/(Time2-Time1)*(Time-Time1); 

		return GaussOutput.reshape((18, self.NumGauss));

	def GaussOutput(self,index):
		""" gets the ESSI Element output at a 
		given Time Step List
		"""

		GaussOutput = np.transpose(np.transpose(self.__HDF5_File['Model/Elements/Gauss_Outputs'][self.IndexToGaussOutput:self.IndexToGaussOutput+self.NumGaussOutput])[index]);

		return GaussOutput;

	def ElementOutput(self,index):
		""" gets the ESSI Element output at a 
		given Time Step List
		"""

		ElementOutput = np.transpose(np.transpose(self.__HDF5_File['Model/Elements/Element_Outputs'][self.IndexToElementOutput:self.IndexToElementOutput+self.NumElementOutput])[index]);

		return ElementOutput

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

	def GaussOutputInfo(self):
		""" shows the output data documentation at gauss points """

		GaussOutputType = ["et_xx","et_yy","et_zz","et_xy","et_yz","et_xz"];
		GaussOutputInfo = ["Total Strain in x-x direction","Total Strain in y-y direction","Total Strain in z-y direction",\
		"Total Strain in x-y direction","Total Strain in y-z direction","Total Strain in x-z direction"];

		GaussOutputType = GaussOutputType + ["ep_xx","ep_yy","ep_zz","ep_xy","ep_yz","ep_xz"];
		GaussOutputInfo = GaussOutputInfo + ["Plastic Strain in x-x direction","Plastic Strain in y-y direction","Plastic Strain in z-y direction",\
		"Plastic Strain in x-y direction","Plastic Strain in y-z direction","Plastic Strain in x-z direction"];

		GaussOutputType = GaussOutputType + ["s_xx","s_yy","s_zz","s_xy","s_yz","s_xz"];
		GaussOutputInfo = GaussOutputInfo + ["Stress in x-x direction","Stress in y-y direction","Stress in z-y direction",\
		"Stress in x-y direction","Stress in y-z direction","Stress in x-z direction"];

		GaussPrint = "\n---------------------------------------\n";
		GaussPrint = GaussPrint + "Gauss Info Element Number -> "+ str(self.Tag) +"\n---------------------------------------\n\t";

		index = 0;
		for index in xrange(0,len(GaussOutputType)):
			GaussPrint = GaussPrint + "["+str(index)+"] :: "+ GaussOutputType[index] + "  " +  GaussOutputInfo[index] + "\n\t";

		# print the information 
		print GaussPrint

	def ElementOutputInfo(self):
		""" shows the output data documentation for element output """

		ElementOutputType, ElementOutputInfo, Status = ESSIclass.ElementOutputInfo(self.ClassTag);

		OutputPrint = "\n---------------------------------------\n";
		OutputPrint = OutputPrint + "Output Info Element Number -> "+ str(self.Tag) +"\n---------------------------------------\n\t";


		if(Status==True):
			if(ElementOutputType==None or ElementOutputInfo==None ):
				OutputPrint =  OutputPrint + self.Name + " does not habve any element output\n";
			else:
				index = 0;
				for index in xrange(0,len(ElementOutputType)):
					OutputPrint = OutputPrint + "["+str(index)+"] :: "+ ElementOutputType[index] + "  " +  ElementOutputInfo[index] + "\n\t";
		else:
			OutputPrint = OutputPrint + "Element Output Info not documented yet\n"

		# print the information 
		print OutputPrint
