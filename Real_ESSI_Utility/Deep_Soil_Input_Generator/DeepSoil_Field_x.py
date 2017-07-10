#/usr/bin/python
###########################################################################################################################
#                                                                                                                         #
#  Generate_DRM :: Python Script to generate DRM Field Motion                                                             #
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -                                      #
#                                                                                                                         #
#                                                                                                                         #
#  GITHUB:: GITHUB:: https://github.com/SumeetSinha/REAL-ESSI_Utility_Tools.git                                           #
#                                                                                                                         #
#                                                                                                                         #
#  Sumeet Kumar Sinha (September,2016)                                                                                    #
#  Computational Geomechanics Group                                                                                       #
#  University of California, Davis                                                                                        #
#  s u m e e t k s i n h a . c o m                                                                                        #
########################################################################################################################### 

import math;
import numpy as np;
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

from openpyxl import *



def getField (x,y,z,DRM_Time):

	TimeVectorSize = DRM_Time.shape[0]; # variables accessible to user  
	acceleration = np.zeros([3, TimeVectorSize],dtype=np.double); # variables accessible to user  
	displacement = np.zeros([3, TimeVectorSize],dtype=np.double); # variables accessible to user  
	time_index = 0;  # variables accessible to user  

	
	############################### Code Starts ########################
	# Deep Soil Input/Output Directory
	Dir = "./DeepSoil_Input_Outputs/";

	# Deep Soil output File 'output.xlsx'
	WorkBookNameX = Dir + "x_motion_output.xlsx";

	Reference_Elevation  = 0; # in meters 

	# Num of Time Steps 
	NumTimeSteps = 10321;
	DeltaT       = 0.0019;
	gravity      = 9.81;

	# Elevation Info File
	Elevation_Info_File = Dir + "Elevation_Info.txt";




	Elevation_Info={}; # elvation map to layers
	Elevation=[]; # elevation info with layer index

	# Coordinates 
	# x = 0;
	# y = 0;
	z = z-Reference_Elevation;

	# Total Number of Layers
	NumLayers = 0;


	DataFile = open(Elevation_Info_File,"r");
	######## Reading the file to get all the Layer Information 
	ParList = 0;
	for line in DataFile.readlines():
		NumLayers = NumLayers+1;
		ParList = re.split('\s',line);
		Elevation_Info[float(ParList[0])] = ParList[1];
		Elevation.append(float(ParList[0]));

	Elevation_Info[float(ParList[0])] = "Top of Rock";
	# print NumLayers;

	# for interpolation 
	first_index = 0;
	second_index = 0;

	print "[getField] :: z = " + str (z);
	interpolated_layers  = "";
	for test_z in Elevation:
		second_index = second_index +1;
		# interpolated_layers = interpolated_layers + "[" + str(test_z) + "] , ";
		if(test_z<=z):
			first_index  = second_index-1;
			break;
	# print interpolated_layers;

	if(first_index==0 and second_index!=1):
		print "[getField] :: Could not find the coordinate z = " + str(z) +"\n";
		exit();

	# Shape Function 
	# N1 ----------------- N2
	# xi = (x - (x1+x2)/2)*2/(x1-x2)

	z1 = Elevation[first_index];
	z2 = Elevation[second_index];
	xi = (z - (z1+z2)/2)*2/(z1-z2)

	sheet_z1 = Elevation_Info[z1];
	sheet_z2 = Elevation_Info[z2];

	print "Interpolation between " + sheet_z1 + " and " + sheet_z2

	# print "[getField] :: Loading workbook " + WorkBookNameX ;
	wb = Workbook();
	wb = load_workbook(WorkBookNameX,read_only=True);


	# print wb.get_sheet_names();
	ws_1 = wb[sheet_z1];
	ws_2 = wb[sheet_z2];

	Numpy_acc_1  = np.zeros([NumTimeSteps],dtype=np.double);
	Numpy_acc_2  = np.zeros([NumTimeSteps],dtype=np.double);
	Numpy_disp_1 = np.zeros([NumTimeSteps],dtype=np.double);
	Numpy_disp_2 = np.zeros([NumTimeSteps],dtype=np.double);
	Numpy_acc    = np.zeros([NumTimeSteps],dtype=np.double);
	Numpy_disp   = np.zeros([NumTimeSteps],dtype=np.double);

	List_time   = np.zeros([NumTimeSteps],dtype=np.double);

	max_row = NumTimeSteps+1;
	max_column = 1;

	row_number = 0;
	column_number = 0;

	disp = 0; 
	vel  = 0; 
	acc  = 0;
	###### Worksheet 1
	for row in ws_1.rows:
		if(row_number == 0):
			row_number=row_number+1;
			continue;
		elif (row_number==max_row):
			break;
		else:
			column_number = 0;
			for cell in row:
				if(column_number==0):
					List_time[row_number-1]= float(cell.value);
				elif (column_number==1):
					acc  = float(cell.value)*gravity;
					Numpy_acc_1[row_number-1] = acc;
					disp = disp + vel*DeltaT + 0.5*acc*DeltaT*DeltaT;
					Numpy_disp_1[row_number-1] = float(disp);
					vel = vel + acc*DeltaT;
				elif(column_number==max_column):
					break;
				column_number = column_number + 1;
		row_number=row_number+1;


	disp = 0; 
	vel  = 0; 
	acc  = 0;
	###### Worksheet 2
	for row in ws_2.rows:
		if(row_number == 0):
			row_number=row_number+1;
			continue;
		elif (row_number==max_row):
			break;
		else:
			column_number = 0;
			for cell in row:
				if (column_number==1):
					acc  = float(cell.value)*gravity;
					Numpy_acc_1[row_number-1] = acc;
					disp = disp + vel*DeltaT + 0.5*acc*DeltaT*DeltaT;
					Numpy_disp_2[row_number-1] = float(disp);
					vel = vel + acc*DeltaT;
				elif(column_number==max_column):
					break;
				column_number = column_number + 1;
		row_number=row_number+1;

	# Now Lets do the interpolation 
	# N1 =  (1+xi)/2
	# N2 =  (1-xi)/2

	N1 = (1+xi)/2;
	N2 =  (1-xi)/2;

	Numpy_acc = N1*Numpy_acc_1 + N2*Numpy_acc_2;
	Numpy_disp = N1*Numpy_disp_1 + N2*Numpy_disp_2;



	#######################################################
	time_index =0;
	for t in DRM_Time:
		t1 = int(t/DeltaT);
		displacement[0,time_index] = Numpy_disp[t1];
		acceleration[0,time_index] = Numpy_acc[t1];
		displacement[1,time_index] = 0;
		acceleration[1,time_index] = 0;
		displacement[2,time_index] = 0;
		acceleration[2,time_index] = 0;
		time_index = time_index +1;


	return displacement, acceleration; # must return 

