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


SectionNumber =1;
Unit ="m";
totalLength = 1.0;
totalWidth = 1.0;
MaterialId = 1;

fiberLength = 0.1 ; 
fiberWidth = 0.1 ; 

NumFiberLen  = (int) (totalLength / fiberLength)  ;
NumFiberWidth = (int) (totalWidth / fiberWidth) ;

NumFibres = 0;
FiberNumber = 0;

fiberArea = fiberWidth * fiberLength ; 
Fiber_Dic = {};

NumReBarLengh = 2 ; 
NumReBarWidth = 2 ; 

ReBarLenghLocs = np.linspace(1, NumFiberLen-2 , NumReBarLengh);
ReBarWidthLocs = np.linspace(1, NumFiberWidth-2 , NumReBarWidth);

for x_id in range(NumFiberLen):
	x = fiberLength / 2.0 + x_id * fiberLength - totalLength/2. 
	for y_id in range(NumFiberWidth):
		y = fiberWidth / 2.0 + y_id * fiberWidth - totalWidth/2. 
		FiberNumber = FiberNumber +1;
		NumFibres   = NumFibres +1;
		New_Fiber = Fiber();
		New_Fiber.Id = FiberNumber;

		if x_id in ReBarLenghLocs and y_id in ReBarWidthLocs :
			New_Fiber.Material_Id = MaterialId + 1;
		else:
			New_Fiber.Material_Id = MaterialId;

		New_Fiber.Section_Id = SectionNumber;
		New_Fiber.Area = fiberArea;
		New_Fiber.X_Coordinate = x;
		New_Fiber.Y_Coordinate = y;
		Fiber_Dic[New_Fiber.Id] = New_Fiber;


##### Writing to the new file 
Filename = "Rectangle_Section_"+str(SectionNumber)+".fei";
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
