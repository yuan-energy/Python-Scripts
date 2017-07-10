#!/usr/bin/env python

"""Module to generate input for DeepSoil
"""

__author__ = "Sumeet K. Sinha"
__credits__ = [""]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Sumeet K. Sinha"
__email__ = "sumeet.kumar507@gmail.com"


import re;
import numpy as np;
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import h5py;
import os;
import sys;
import importlib;
import shutil;

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


# user Input 
RefMotionName = "motion";   # motion filename usede in DeepSoil 'motion.dat'
RefSurfaceElevation  = 0;   # in meters 

SoilLayerDataFile   = "Soil_Layer_Data.dat";

print "#################################################################################"
print "#                                                                               #"
print "#  Generate_DeepSoil_Input :: Generate Input for Deep Soil   for                #"
print "#                  given file containg Soil Layer Data                          #"
print "#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#"
print "#                                                                               #"
print "#                                                                               #"
print "#  GITHUB:: https://github.com/SumeetSinha/REAL-ESSI_Utility_Tools.git          #"
print "#                                                                               #"
print "#                                                                               #"
print "#  Sumeet Kumar Sinha (March,2017)                                              #"
print "#  Computational Geomechanics Group                                             #"
print "#  University of California, Davis                                              #"
print "#  s u m e e t k s i n h a . c o m                                              #"
print "#################################################################################\n\n\n"

SoilLayerDataFile = raw_input("Please enter your soil layer data file name:: ");
# print SoilLayerDataFile
if(not(os.path.exists(SoilLayerDataFile)) or not(os.path.isfile(SoilLayerDataFile))):
	print "ERROR:: File does not Exist"
	print "ABORTING!!"
	exit();

# RefMotionName            = raw_input("Reference motion filename to be used in DeepSoil :: ");
RefSurfaceElevation      = float(raw_input("Reference Surface Elevation [m]:: "));

DataFile = open(SoilLayerDataFile,"r");

# map containing elevation and deconvulation output file  
Z_Elevation_Dic={};
Z_Elevation_Vec=[];


# status of program 
status = 1 # success

LayerNo = 0;
Elevation = 0;
LineNo = 0;

# variables 
Thickness=[]
Unit_Weight=[]
Shear_Velocity=[]
Num_Points=[]
Damping=[]

print "\n[Generate_Deconvulation_Input]:: Reading File \"" + SoilLayerDataFile + "\" to get Soil Layers Data";

######## Reading the file to get all the DRM Elements 
for line in DataFile.readlines():

	LineNo = LineNo+1;
	ParList = re.split('\s*|\t*|\n*',line);
	If_Float = isfloat(ParList[0]);

	NumTokens = len(ParList);

	# The command is add element command
	if (If_Float):
		if (NumTokens>=5):
			Thickness.append(float(ParList[0]));
			Unit_Weight.append(float(ParList[1]));
			Shear_Velocity.append(float(ParList[2]));
			Num_Points.append(int(ParList[3]));
			Damping.append(float(ParList[4]));

			LayerNo = LayerNo+1;
			Z_Elevation_Vec.append(Elevation);
			# Z_Elevation_Dic[Elevation] = "Deconvolved - " + RefMotionName + " - layer "+str(LayerNo)+".txt"; # Depretiated [Sumeet, April, 2017]
			Z_Elevation_Dic[Elevation]= "Layer"+str(LayerNo);
			Elevation = Elevation - float(ParList[0]);
		else:
			print "\nWARNING:: [Generate_Deconvulation_Input]:: Error in Line no " + str(LineNo) + " Skipping it !! \n " ; 	

Z_Elevation_Vec.append(Elevation);
Z_Elevation_Dic[Elevation] = "Layer"+str(LayerNo+1); # rocklayer 
DataFile.close();

print "\n[Generate_Deconvulation_Input]:: Total Number of Layers Found are  " + str (LayerNo);
print "\n[Generate_Deconvulation_Input]:: Started Generating Deconvulation Input File \" DeepSoil_Deconvulation_Input.dp\"";

######## Start Generating the DeepSoil Input File
output_file =  "Copy_Contents_To_DeepSoil_Input_File.dp";
DeepSoilinputFile = open(output_file,"w");

# writting the header of the file 
print "\n[Generate_Deconvulation_Input]:: Writing the Input header\n";
DeepSoilinputFile.write("[FILE_VERSION]:[1]\n");
DeepSoilinputFile.write("[ANALYSIS_DOMAIN]:[FREQUENCY]\n");
DeepSoilinputFile.write("[ANALYSIS_TYPE]:[LINEAR]\n");
DeepSoilinputFile.write("[SHEAR_TYPE]:[VELOCITY]\n");
DeepSoilinputFile.write("[MAX_ITERATIONS]:[1]\n");
DeepSoilinputFile.write("[ERROR_TOL]:[0.00001]\n");
DeepSoilinputFile.write("[COMPLEX_MOD]:[SHAKE_FI]\n");
DeepSoilinputFile.write("[EFFECTIVE_SSR]:[0.65]\n");
DeepSoilinputFile.write("[DYNAMIC_CURVES]:[DISCRETE_POINTS]\n");
DeepSoilinputFile.write("[NUM_LAYERS]:["+str(LayerNo)+"]\n");
DeepSoilinputFile.write("[WATER_TABLE]:[0]\n");

LayerNoInfo = 0;

for Thickness_item in Thickness:
	
	DeepSoilinputFile.write("[LAYER]:["+str(LayerNoInfo+1)+"]\n");
	Thickness_Info = "[THICKNESS]:["+str(Thickness[LayerNoInfo])+"]";
	Weight_Info = "[WEIGHT]:["+str(Unit_Weight[LayerNoInfo])+"]";
	Shear_Info = "[SHEAR]:["+str(Shear_Velocity[LayerNoInfo])+"]";
	NumPoints_Info = "[NUM_POINTS]:[2]";
	line_new = "%13s %-27s %-27s %-27s %-27s\n" % ("",Thickness_Info, Weight_Info,Shear_Info,NumPoints_Info);
	DeepSoilinputFile.write(line_new);
	Dynamic_Curve_Strain_Info = "[DYNAMIC_CURVE]:[STRAIN]";
	Strain_Info_1 = "[1E-05]";
	Strain_Info_2 = "[0.1]";
	line_new = "%13s %-27s %-13s %-13s\n" % ("",Dynamic_Curve_Strain_Info, Strain_Info_1,Strain_Info_2);
	DeepSoilinputFile.write(line_new);
	Dynamic_Curve_Modulus_Info = "DYNAMIC_CURVE]:[MODULUS]";
	Modulus_Info_1 = "[1]";
	Modulus_Info_2 = "[1]";
	line_new = "%13s %-27s %-13s %-13s\n" % ("",Dynamic_Curve_Modulus_Info, Modulus_Info_1,Modulus_Info_2);
	DeepSoilinputFile.write(line_new);
	Dynamic_Curve_Damping_Info = "DYNAMIC_CURVE]:[DAMPING]";
	Damping_Info_1 = "["+str(Damping[LayerNoInfo]/100)+"]";
	Damping_Info_2 = "["+str(Damping[LayerNoInfo]/100)+"]";
	line_new = "%13s %-27s %-13s %-13s\n" % ("",Dynamic_Curve_Damping_Info, Damping_Info_1,Damping_Info_2);
	DeepSoilinputFile.write(line_new);
	Output_Info = "[OUTPUT]:[TRUE]";
	line_new = "%13s %-27s\n" % ("",Output_Info);
	DeepSoilinputFile.write(line_new);
   	LayerNoInfo = LayerNoInfo +1;	
	print "\n[Generate_Deconvulation_Input]:: Layer No [ " + str(LayerNoInfo) +" ] completed .."

print "\n[Generate_Deconvulation_Input]:: Writing the Input Footer\n";
DeepSoilinputFile.write("[HALFSPACE]:[ELASTIC]       [UNIT_WEIGHT]:[160]         [SHEAR]:[5000]              [DAMPING]:[0.02]\n");
DeepSoilinputFile.write("[RS_TYPE]:[FREQUENCY]       [RS_DAMPING]:[0.05]\n");
DeepSoilinputFile.write("[ACCELERATION_HISTORY]:[EXTERNAL] [DEEPSOILACCELINPUT.TXT]\n");
DeepSoilinputFile.write("[UNITS]:[METRIC]\n");
DeepSoilinputFile.write("[LAYER_NAMES]:[0]\n");

print "\n[Generate_Deconvulation_Input]:: Input File !!!!!!! Sucessfully Written !!!!!!\n";

DeepSoilinputFile.close();

# dst = "Input.dp";
# shutil.copy2(output_file, dst);
# os.remove(output_file);

# # if not os.path.exists('/Deep_Soil_Input_Output'):
# #     os.mkdir('/Deep_Soil_Input_Output')
# # shutil.copy2(dst,"/Deep_Soil_Input_Output");

################ Writing Elevation Info 
print "\n[Generate_Deconvulation_Input]:: Writing about the layer output results info \n";

Elevation_InfoFile = open("Elevation_Info.txt","w");
i = 1;
for x in Z_Elevation_Vec:
	Elevation_InfoFile.write(str(x) + "\t" + str(Z_Elevation_Dic[x])+"\n");
Elevation_InfoFile.close();
