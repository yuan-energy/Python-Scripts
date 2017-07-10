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
from   nodeFile  import *;
from   nodeInfo  import *;
from   nodeDisp   import *;
from   nodeAcc   import *;
from   nodeDof   import *;

class node:
	'It represents an REAL-ESSI Node'

	tag                   = -1;
	coord                 = -1;
	numDof                = -1;
	processId             = -1;
	__Time                = None;
	indexToOutput         = -1;
	file                  = None;
	__HDF5_File           = None;
	dofType               = None;

	def __str__(self):
		return nodeInfo(self.file,self.tag);

	def __init__ (self,file,tag):
		""" Define ESSInode class with output file

		Class Variables:
		tag -- REAL ESSI Node stag
		file   -- HDF5 output file 
		"""

		self.tag  = tag;
		self.file = nodeFile(file,tag);
		self.__initialize();


	def __initialize(self):
		""" Initializes the variables by getting data from 
		HDF5 output file
		"""
		self.__HDF5_File        = h5py.File(self.file, 'r');
		Index_to_Coordinates    = self.__HDF5_File['Model/Nodes/Index_to_Coordinates'][self.tag];
		self.coord        = self.__HDF5_File['Model/Nodes/Coordinates'][Index_to_Coordinates:Index_to_Coordinates+3];
		self.indexToOutput      = self.__HDF5_File['Model/Nodes/Index_to_Generalized_Displacements'][self.tag];
		self.numDof            = self.__HDF5_File['Model/Nodes/Number_of_DOFs'][self.tag];
		self.processId          = self.__HDF5_File['Process_Number'][0];

		if (self.numDof==3):
			self.dofType, DofInfo = self.__DispInfo3DOF();
		elif (self.numDof==4):
			self.dofType, DofInfo = self.__DispInfo4DOF();
		elif (self.numDof==6):
			self.dofType, DofInfo = self.__DispInfo6DOF();
		elif (self.numDof==7):
			self.dofType, DofInfo = self.__DispInfo7DOF();


	def Dof(self,index=None):
		""" returns the dof output of the 
		Real ESSI node tag """

		return nodeDof(self.file,self.tag,index);

	def RelDof(self,relIndex=0,index=None):
		""" returns the dof output of the 
		Real ESSI node tag relative to a index"""

		return nodeRelDof(self.file,self.tag,relIndex,index);

	def Disp(self,index=None):
		""" returns the displacement output of the 
		Real ESSI node tag """

		return nodeOutpt(self.file,self.tag,index);

	def RelDisp(self,relIndex=0,index=None):
		""" returns the displacement output of the 
		Real ESSI node tag relative to a index"""

		return nodeRelOutpt(self.file,self.tag,relIndex,index);

	def Info(self):
		""" returns the information about node as string"""

		return nodeInfo(self.file,self.tag);



















































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
