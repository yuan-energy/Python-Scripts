#!/usr/bin/env python

"""Module to return information about ESSI element

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

def ele(file,tag):
	""" returns information about any given ESSI
	node and file
	"""
	return eleInfo(file,tag)

def eleInfo(file,tag):
	""" returns information about any given ESSI
	node and file
	"""

	# get the element file 
	ElementFile                  = eleFile(file,tag);

	# return None if element file is not correct
	if (ElementFile is None):
		return None;

	HDF5_File               = h5py.File(ElementFile, 'r');
	Index_to_Connectivity   = HDF5_File['Model/Elements/Index_to_Connectivity'][tag];
	IndexToElementOutput    = HDF5_File['Model/Elements/Index_to_Element_Outputs'][tag];
	IndexToGaussOutput      = HDF5_File['Model/Elements/Index_to_Gauss_Point_Coordinates'][tag]*18/3;
	ClassTag                = HDF5_File['Model/Elements/Class_Tags'][tag];
	ClassTagDesc            = ELE_TAG_DESC_ARRAY[ClassTag];
	Name                    = str.strip(ELE_NAME[ClassTag-1]);
	MaterialTag             = HDF5_File['Model/Elements/Material_Tags'][tag];
	NumNodes                = NUMBER_OF_NODES(ClassTagDesc);
	NumGauss                = NUMBER_OF_GAUSS(ClassTagDesc);
	NumGaussOutput          = NumGauss*18;
	NumElementOutput        = NUMBER_OF_ELEMENT_OUTPUTS(ClassTagDesc);
	Connectivity            = HDF5_File['Model/Elements/Connectivity'][Index_to_Connectivity:Index_to_Connectivity+NumNodes];
	ProcessId               = HDF5_File['Process_Number'][0];

	eleOutputType, eleOutputInfo, Status = ElementOutputInfo(ClassTag);
	GaussOutputType = ["et_xx","et_yy","et_zz","et_xy","et_yz","et_xz"];
	GaussOutputType = GaussOutputType + ["ep_xx","ep_yy","ep_zz","ep_xy","ep_yz","ep_xz"];
	GaussOutputType = GaussOutputType + ["s_xx","s_yy","s_zz","s_xy","s_yz","s_xz"];

	if(NumGauss>0):
		GaussPointCoordinates   = (HDF5_File['Model/Elements/Gauss_Point_Coordinates'][IndexToGaussOutput/18*3:IndexToGaussOutput/18*3+3*NumGauss]).reshape((3,NumGauss));


	printInfo =  "\
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
" % (Name, tag,Connectivity,NumNodes,NumGauss,\
	MaterialTag,NumElementOutput,NumGaussOutput,eleOutputType,\
	GaussOutputType,IndexToGaussOutput,IndexToElementOutput,\
	ClassTag,ClassTagDesc,ProcessId,ElementFile) + "\n " + __GaussOutputInfo(tag) +\
	"\n"+__ElementOutputInfo(tag,ClassTag,Name)+"\n"

	return printInfo;


def __GaussOutputInfo(tag):
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
	GaussPrint = GaussPrint + "Gauss Info Element Number -> "+ str(tag) +"\n---------------------------------------\n\t";

	index = 0;
	for index in xrange(0,len(GaussOutputType)):
		GaussPrint = GaussPrint + "["+str(index)+"] :: "+ GaussOutputType[index] + "  " +  GaussOutputInfo[index] + "\n\t";

	# return the information
	return GaussPrint

def __ElementOutputInfo(tag,ClassTag,Name):
	""" shows the output data documentation for element output """

	eleOutputType, eleOutputInfo, Status = ElementOutputInfo(ClassTag);

	OutputPrint = "\n---------------------------------------\n";
	OutputPrint = OutputPrint + "Output Info Element Number -> "+ str(tag) +"\n---------------------------------------\n\t";


	if(Status==True):
		if(eleOutputType==None or eleOutputInfo==None ):
			OutputPrint =  OutputPrint + Name + " does not habve any element output\n";
		else:
			index = 0;
			for index in xrange(0,len(eleOutputType)):
				OutputPrint = OutputPrint + "["+str(index)+"] :: "+ eleOutputType[index] + "  " +  eleOutputInfo[index] + "\n\t";
	else:
		OutputPrint = OutputPrint + "Element Output Info not documented yet\n"

	# return the information 
	return OutputPrint
