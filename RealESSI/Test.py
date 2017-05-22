#!/usr/bin/env python

"""This Script as name suggests tests all the functions of the modules

The models considered here are RealESSI, ESSIelement, ESSInode, ESSItime,
ESSIinput, ESSIoutput. The input files for the scripts are present in 
Input_Files directory
"""

__author__ = "Sumeet K. Sinha"
__credits__ = [""]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Sumeet K. Sinha"
__email__ = "sumeet.kumar507@gmail.com"

from RealESSI import *;


SequentialFeioutputFilename = './Input_Files/Beam_Axial_Load.h5.feioutput';
ParallelFeioutputFileName = './Input_Files/NPPModel_DRM_Motion.h5.feioutput';


Sequential = RealESSI(SequentialFeioutputFilename);
Parallel   = RealESSI(ParallelFeioutputFileName);
print Sequential;
print Parallel;





