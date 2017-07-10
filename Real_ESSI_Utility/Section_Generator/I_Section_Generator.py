
###########################################################################################################################
#                                                                                                                         #
#                               I_Section_Generator                                                                       #
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -                                      #
#                                                                                                                         #
#  GITHUB:: https://github.com/SumeetSinha/REAL-ESSI_Utility_Tools                                                        #
#                                                                                                                         #
#  Sumeet Kumar Sinha (April,2017)                                                                                        #
#  Computational Geomechanics Group                                                                                       #
#  University of California, Davis                                                                                        #
#  s u m e e t k s i n h a . c o m                                                                                        #
########################################################################################################################### 

import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import matplotlib.patches as patches
from matplotlib import interactive
import numpy as np
import h5py
import sys
import re
import math
import matplotlib.cm as cm

class Fiber:
  Id          = 0
  Material_Id = 0
  Section_Id  = 0
  X_Coordinate = 0
  Y_Coordinate = 0
  Area         = 0
  Radius       = 0

  def __repr__(self):
  	return "Fibre No: %s \n\t Material_Id: %s \n\t Section_Id: %s \n\t X_Coordinate: %s \n\t Y_Coordinate: %s \n\t Radius: %s \n" % (self.Id, self.Material_Id, self.Section_Id, self.X_Coordinate, self.Y_Coordinate, self.Radius)


print "#################################################################################";
print "#                                                                               #"
print "#  I_Section_Generator :: Generates I section fiber elements for given          #"
print "#                  section dimensions and mesh lengths                          #"
print "#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#"
print "#                                                                               #"
print "#                                                                               #"
print "#  GITHUB:: https://github.com/SumeetSinha/REAL-ESSI_Utility_Tools.git          #"
print "#                                                                               #"
print "#                                                                               #"
print "#  Sumeet Kumar Sinha (April,2017)                                              #"
print "#  Computational Geomechanics Group                                             #"
print "#  University of California, Davis                                              #"
print "#  s u m e e t k s i n h a . c o m                                              #"
print "#################################################################################\n\n\n";


# print ("\n ------------------------ Defining I Section -----------------------------------\n \n" );

# SectionNumber  = int(raw_input("I Section Number :: "));
# Unit           = raw_input("Geometry File Unit of Section :: ");
# Flange_Width   = float(raw_input("Width of the flange :: "));
# Flange_Thickness;   = float(raw_input("Thickness of the Flange :: "));
# Web_Thickness     = float(raw_input("Thickness of the Web :: "));
# Depth              = float(raw_input("Depth of Section :: "));
# MaterialId         = raw_input("Material Id of Section :: ");


# print ("\n\n ------------------------ Defining Mesh Parameters -----------------------------------\n \n" );

# NumEle_Flange_Thickness  = int(raw_input("Nnumber of fibers in Flange Thickness :: "));
# NumEle_Flange_Width      = int(raw_input("Nnumber of fibers in Flange Width :: "));
# NumEle_Web_Thickness  = int(raw_input("Nnumber of fibers in Web Thickness :: "));
# NumEle_Web_Depth      = int(raw_input("Nnumber of fibers in Web Depth :: "));


SectionNumber =1;
Unit ="m";
Flange_Width = 10.0;
Flange_Thickness = 2.0;
Web_Thickness = 2.0;
Depth= 10;
MaterialId = 1;
NumEle_Flange_Thickness= 2;
NumEle_Flange_Width= 10;
NumEle_Web_Thickness= 2;
NumEle_Web_Depth=6;


Web_Depth = float(Depth -2*Flange_Thickness);

# parameters 
NumFibres = 0;
FiberNumber = 0;
X_Coord =0;
Y_Coord =0;
Area    =0;
radius  =0;

flange_y_begin = float(Web_Depth/2);
flange_y_end   = float(Web_Depth/2+NumEle_Flange_Thickness);

flange_x = np.arange(float(-Flange_Width/2),float(Flange_Width/2)+float(Flange_Width)/(NumEle_Flange_Width),float(Flange_Width)/(NumEle_Flange_Width));
flange_y = np.arange(flange_y_begin,flange_y_end+float(Flange_Thickness)/(NumEle_Web_Thickness),float(Flange_Thickness)/(NumEle_Web_Thickness));

web_y = np.arange(float(-Web_Depth/2),float(Web_Depth/2)+Web_Depth/(NumEle_Web_Depth),Web_Depth/(NumEle_Web_Depth));
web_x = np.arange(-float(Web_Thickness/2),float(Web_Thickness/2)+float(Web_Thickness)/(NumEle_Web_Thickness),float(Web_Thickness)/(NumEle_Web_Thickness));

# print flange_x;
# print web_y;
# print web_x;
# print flange_y;
Fiber_Dic = {};


flange_fiber_area=(Flange_Width*Flange_Thickness)/(NumEle_Flange_Thickness*NumEle_Flange_Width);
web_fiber_area   =(Web_Depth*Web_Thickness)/(NumEle_Web_Thickness*NumEle_Web_Depth);

####### Building (+ve) flange fiber  ##########
for i in range(0,NumEle_Flange_Thickness):
	y = float(flange_y[i]+flange_y[i+1])/2;

	for j in range(NumEle_Flange_Width):
		x = float(flange_x[j]+flange_x[j+1])/2;

		FiberNumber = FiberNumber +1;
		NumFibres   = NumFibres +1;
		New_Fiber = Fiber();
		New_Fiber.Id = FiberNumber;
		New_Fiber.Material_Id = MaterialId;
		New_Fiber.Section_Id = SectionNumber;
		New_Fiber.Area = flange_fiber_area;
		New_Fiber.Radius = math.sqrt(float(flange_fiber_area));
		New_Fiber.X_Coordinate = x;
		New_Fiber.Y_Coordinate = y;
		Fiber_Dic[New_Fiber.Id] = New_Fiber;

####### Building flange fiber  ##########
for i in range(0,NumEle_Web_Depth):
	y = float(web_y[i]+web_y[i+1])/2;

	for j in range(NumEle_Web_Thickness):
		x = float(web_x[j]+web_x[j+1])/2;

		FiberNumber = FiberNumber +1;
		NumFibres   = NumFibres +1;
		New_Fiber = Fiber();
		New_Fiber.Id = FiberNumber;
		New_Fiber.Material_Id = MaterialId;
		New_Fiber.Section_Id = SectionNumber;
		New_Fiber.Area = web_fiber_area;
		New_Fiber.Radius = math.sqrt(float(web_fiber_area));
		New_Fiber.X_Coordinate = x;
		New_Fiber.Y_Coordinate = y;
		Fiber_Dic[New_Fiber.Id] = New_Fiber;

####### Building (-ve) flange fiber  ##########
for i in range(0,NumEle_Flange_Thickness):
	y = -(flange_y[i]+flange_y[i+1])/2;

	for j in range(NumEle_Flange_Width):
		x = (flange_x[j]+flange_x[j+1])/2;
		
		FiberNumber = FiberNumber +1;
		NumFibres   = NumFibres +1;
		New_Fiber = Fiber();
		New_Fiber.Id = FiberNumber;
		New_Fiber.Material_Id = MaterialId;
		New_Fiber.Section_Id = SectionNumber;
		New_Fiber.Area = flange_fiber_area;
		New_Fiber.Radius = math.sqrt(float(flange_fiber_area));
		New_Fiber.X_Coordinate = x;
		New_Fiber.Y_Coordinate = y;
		Fiber_Dic[New_Fiber.Id] = New_Fiber;


##### Writing to the new file 
Filename = "Section_"+str(SectionNumber)+".fei";
NewSectionFile = open(Filename,"w"); 
 
for x in Fiber_Dic:
	NewFiber = Fiber_Dic[x];
	Cord_X = str(NewFiber.X_Coordinate)+"*"+Unit;
	Cord_Y = str(NewFiber.Y_Coordinate)+"*"+Unit;
	Area   = str(NewFiber.Area)+"*"+Unit+"^2";
	# print Fiber_Dic[x];
	cmd = "add fiber # "+str(NewFiber.Id)+" using material # "+str(NewFiber.Material_Id)+" to section # "+str(NewFiber.Section_Id)+" fiber_cross_section = "+Area+" fiber_location = ("+Cord_X+", "+ Cord_Y+");\n";
	NewSectionFile.write(cmd); 

NewSectionFile.close();
