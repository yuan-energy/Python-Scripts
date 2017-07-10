
###########################################################################################################################
#                                                                                                                         #
#                               Plot Cross Sections                                                                       #
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -                                      #
#                                                                                                                         #
#  GITHUB:: https://github.com/SumeetSinha/REAL-ESSI_Utility_Tools                                                        #
#                                                                                                                         #
#  Sumeet Kumar Sinha (January,2017)                                                                                      #
#  Computational Geomechanics Group                                                                                       #
#  University of California, Davis                                                                                        #
#  s u m e e t k s i n h a . c o m                                                                                        #
########################################################################################################################### 

from __future__ import print_function
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

if len(sys.argv) == 1:
	print ("You can also give filename as a command line argument")
	filename = raw_input("Enter Filename: ")
else:
	filename = sys.argv[1]

Cross_Section_Id = {};
Fiber_Dic = {};

with open(filename) as f:
	full_line = "";
	activate  = 0;
	for line in f:
		full_line = full_line + line;
		if ("addfiber#" in line.replace(" ", "")) :
			full_line = line;
			activate = 1;
		if  (";" in line.replace(" ", "")) :
			if (activate ==1):
				Split_List = re.split(' |\n|\t|\*|\(',full_line)
				full_line = ""
				New_Fiber = Fiber();
				New_Fiber.Id = Split_List[3]
				New_Fiber.Material_Id = Split_List[7]
				New_Fiber.Section_Id = Split_List[11]
				New_Fiber.Area = Split_List[14]
				New_Fiber.Radius = math.sqrt(float(Split_List[14]))
				New_Fiber.X_Coordinate = Split_List[19]
				New_Fiber.Y_Coordinate = Split_List[21]
				# print (Split_List)
				# print (repr(New_Fiber))

				# get fibre_list_if for the crossection 
				Fiber_Dic[New_Fiber.Id] = New_Fiber;
				fiber_list = [];
				if New_Fiber.Section_Id in Cross_Section_Id:
					fiber_list =  Cross_Section_Id[New_Fiber.Section_Id]
				fiber_list.append(New_Fiber.Id)
				Cross_Section_Id[New_Fiber.Section_Id] = fiber_list;

colours = ["blue","green","red","cyan","magenta","yellow","black","white"]

for cs in Cross_Section_Id:
	fiber_list = Cross_Section_Id[cs]
	fig, ax = plt.subplots() 
	x_min = -.5
	x_max = .5
	y_min = -.5
	y_max = .5
	# print (fiber_list)
	for f in fiber_list:
		fiber = Fiber_Dic[f]
		# if int(fiber.Material_Id)==1:
		# rect = patches.Rectangle((float(fiber.X_Coordinate),float(fiber.Y_Coordinate)),float(fiber.Radius),float(fiber.Radius),linewidth=2,edgecolor='black',facecolor=colours[int(fiber.Material_Id)-1])
		rect = patches.Rectangle((float(fiber.X_Coordinate) - float(fiber.Radius)/2.0,float(fiber.Y_Coordinate) - float(fiber.Radius)/2.0),float(fiber.Radius),float(fiber.Radius),linewidth=2,edgecolor='black',facecolor=colours[int(fiber.Material_Id)-1])
		ax.add_patch(rect)
		# print (fiber.Material_Id)

	legend_patch_list = [];
	i = 0;
	for c in colours:
		legend_patch_list.append(patches.Patch(color=c, label=str(i+1)))
		i = i+1;

	plt.legend(loc="upper left", title="Material_Id", handles=legend_patch_list)
	plt.axis('tight')
	plt.xlabel('X Coordinates')
	plt.ylabel('Y Coordinates')
	plt.show()
	fig.tight_layout()
	fig.savefig('Crossection_'+str(cs)+'.png')		

