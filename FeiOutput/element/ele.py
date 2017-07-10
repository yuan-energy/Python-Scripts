#!/usr/bin/env python

"""Module to return Real ESSI ele class
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
from   element  import *;

class ele:
	'It represents an REAL-ESSI element'

	tag                   = -1;
	connectivity          = -1;
	materialTag           = -1;
	classTag              = -1;
	name                  = "CompGeoMechanicUCDElement";
	processId             = -1;
	classTagDesc          = -1;
	indexToGaussOutput    = None;
	indexToElementOutput  = None;
	file                  = None;
	gaussCoord            = None;
	numNode               =  0;
	numGauss              =  0;
	numGaussOutput        =  0;
	numElementOutput      =  0;
	__HDF5_File			  = None;
	gaussOutputType       = None;
	eleOutptType          = None;


	def __str__(self):
		return eleInfo(self.file,self.tag);

	def __init__ (self,file,tag):
		""" Define Real ESSI element class

		Class Variables:
		file   -- HDF5 output file 
		tag    -- REAL ESSI Element tag
		"""

		self.tag  = tag;
		self.file = eleFile(file,tag);
		self.__initialize();


	def __initialize(self):
		""" Initializes the variables by getting data from 
		HDF5 output file
		"""
		self.__HDF5_File             = h5py.File(self.file, 'r');
		Index_to_Connectivity        = self.__HDF5_File['Model/Elements/Index_to_Connectivity'][self.tag];
		self.indexToElementOutput    = self.__HDF5_File['Model/Elements/Index_to_Element_Outputs'][self.tag];
		self.indexToGaussOutput      = self.__HDF5_File['Model/Elements/Index_to_Gauss_Point_Coordinates'][self.tag]*18/3;
		self.classTag                = self.__HDF5_File['Model/Elements/Class_Tags'][self.tag];
		self.classTagDesc            = ELE_TAG_DESC_ARRAY[self.classTag];
		self.name                    = str.strip(ELE_NAME[self.classTag-1]);
		self.materialTag             = self.__HDF5_File['Model/Elements/Material_Tags'][self.tag];
		self.numNode                 = NUMBER_OF_NODES(self.classTagDesc);
		self.numGauss                = NUMBER_OF_GAUSS(self.classTagDesc);
		self.numGaussOutput          = self.numGauss*18;
		self.numElementOutput        = NUMBER_OF_ELEMENT_OUTPUTS(self.classTagDesc);
		self.connectivity            = self.__HDF5_File['Model/Elements/Connectivity'][Index_to_Connectivity:Index_to_Connectivity+self.numNode];
		self.processId               = self.__HDF5_File['Process_Number'][0];
		
		self.eleOutptType, eleOutputInfo, Status = ElementOutputInfo(self.classTag);
		self.gaussOutputType = ["et_xx","et_yy","et_zz","et_xy","et_yz","et_xz"];
		self.gaussOutputType = self.gaussOutputType + ["ep_xx","ep_yy","ep_zz","ep_xy","ep_yz","ep_xz"];
		self.gaussOutputType = self.gaussOutputType + ["s_xx","s_yy","s_zz","s_xy","s_yz","s_xz"];

		if(self.numGauss>0):
			self.gaussCoord   = (self.__HDF5_File['Model/Elements/Gauss_Point_Coordinates'][self.indexToGaussOutput/18*3:self.indexToGaussOutput/18*3+3*self.numGauss]).reshape((3,self.numGauss));

	def Gauss(self,index=None):
		""" returns the gauss output of the 
		Real ESSI element tag """

		return eleGauss(self.file,self.tag,index);

	def RelGauss(self,relIndex=0,index=None):
		""" returns the gauss output of the 
		Real ESSI element tag relative to a index"""

		return eleRelGauss(self.file,self.tag,relIndex,index);

	def Outpt(self,index=None):
		""" returns the element output of the 
		Real ESSI element tag """

		return eleOutpt(self.file,self.tag,index);

	def RelOutpt(self,relIndex=0,index=None):
		""" returns the element output of the 
		Real ESSI element tag relative to a index"""

		return eleRelOutpt(self.file,self.tag,relIndex,index);

	def Info(self):
		""" returns the information about element as string"""

		return eleInfo(self.file,self.tag);