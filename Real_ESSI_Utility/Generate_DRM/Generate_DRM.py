
#!/usr/bin/env python

"""This Script generates DRM Motions

The drm motions are generated for a given symmetric cuboidal geometry
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


# Defining Node Class
class Node:
	Id = 0;
	Xcord = 0.0;
	Ycord = 0.0;
	Zcord = 0.0;
	Flag  = 0  ; # 1 for interior node # 0 for exterior node 

	def __str__(self):
		message = "";
		message = message + "Node No = " + str(self.Id) + "\n";
		message = message + "\t X Coordinate = " + str(self.Xcord) + "\n"
		message = message + "\t Y Coordinate = " + str(self.Ycord) + "\n"
		message = message + "\t Z Coordinate = " + str(self.Zcord)+ "\n \n"
		return message;

# Defining Element Class
class Element:
	Id = 0;
	NumNodes =  0;
	NodeList = [0,1,6];
	Type     = " ";
	Material = 0;

	def __str__(self):
		message = "";
		message = message + "Element No = " + str(self.Id) + "\n";
		message = message + "\t Type = " + self.Type + "\n";
		message = message + "\t Num of Nodes = " + str(self.NumNodes) + "\n"
		message = message + "\t Node List    = " + str(self.NodeList) + "\n"
		message = message + "\t Material No  = " + str(self.Material) + "\n"
		return message;


def check (coord, min_coord, max_coord, Tol):
	result = 0; # means fail 
	if( (min_coord <= coord  and coord <= max_coord) or (min_coord <= (coord+Tol)  and (coord+Tol)  <= max_coord) or (min_coord <= (coord-Tol)   and (coord-Tol)  <= max_coord) ):
		result = 1;

	return result;

def Generate_DRM(GeometryFile="geometry.fei",DrmMaterial=8,WidthX=5,WidthY=5,WidthZ=5,GF_Unit_To_SI_Unit=1,Tol=1,MotionName='M5_5',OutputPath='./',TestNodeNum=None):

	# print GeometryFile
	if(not(os.path.exists(GeometryFile)) or not(os.path.isfile(GeometryFile))):
		print "ERROR:: File does not Exist"
		print "ABORTING!!"
		exit();

	GeometryFileId = open(GeometryFile,"r");

	# objects of node and element class
	element = Element();
	node    = Node();

	# map containing node and element list 
	ElementList ={};
	NodeList    ={};
	X_Coordinate=[];
	Y_Coordinate=[];
	Z_Coordinate=[];

	# Numpy Arrays
	DRM_Elements = np.empty((0),dtype=np.int32);
	DRM_Nodes = np.empty((0),dtype=np.int32);
	DRM_Whether_Boundary_Node = np.empty((0),dtype=np.int32);

	# status of program 
	status = 1 # success

	NumElements = 0;
	NumNodes    = 0;
	NumExteriorNodes = 0;
	NumInteriorNodes = 0;

	# bounds 
	max_X_Coordinate = 0 ;
	max_Y_Coordinate = 0 ;
	max_Z_Coordinate = 0 ;
	min_X_Coordinate = 0 ;
	min_Y_Coordinate = 0 ;
	min_Z_Coordinate = 0 ;

	print "\n[Generate_DRM]:: Reading File \"" + GeometryFile + "\" to get DRM Elements";

	######## Reading the file to get all the DRM Elements 
	for line in GeometryFileId.readlines():

		ParList = re.split('\s*;\s*|\s*=\s*|\s*#\s*|\s*\(\s*|\s*\)\s*|\s+|\s*,\s*|\s*;\s*|',line);
		Command = ParList[0] + "_" + ParList[1];

		NumTokens = len(ParList);
		TempNodeList = [];

		# The command is add element command
		if(Command=="add_element"):

			# print ParList;
			element = Element();

			for TokenNo in range(0,NumTokens):
				token = ParList[TokenNo];
				if(token=="element"):
					TokenNo = TokenNo+1;
					token = ParList[TokenNo];
					element.Id = int(token);
				if(token=="type"):
					TokenNo = TokenNo+1;
					token = ParList[TokenNo];
					element.Type = token;
				if(token=="nodes"):
					TokenNo = TokenNo+1;
					token = ParList[TokenNo];
					while(token.isdigit()):
						TempNodeList.append(int(token));
						TokenNo = TokenNo+1;
						token = ParList[TokenNo];
					element.NodeList = TempNodeList;
					element.NumNodes = len(TempNodeList);
				if(token=="material"):
					TokenNo = TokenNo+1;
					token = ParList[TokenNo];
					element.Material = token;

			if(element.Material == str(DrmMaterial)):
				if element.Id not in ElementList:
					ElementList[element.Id] = element;
					DRM_Elements = np.append(DRM_Elements,element.Id);
					NumElements = NumElements +1;
					for n in TempNodeList:
						NodeList[n] = node; # initializing nodes
				else:
					print "\nWARNING:: [Generate_DRM]:: Element No " + str(element.Id) + "allready initialized. Ignoring IT!! "; 	


	GeometryFileId.close();

	print "\n[Generate_DRM]:: Total Number of DRM Elements Found are  " + str (NumElements);
	print "\n[Generate_DRM]:: Total Number of DRM Nodes Found are  " + str (len(NodeList));
	print "\n[Generate_DRM]:: Reading File \"" + GeometryFile + "\" again to get DRM Nodes";

	######## Again Start Reading to get only the required nodes 
	GeometryFileId = open(GeometryFile,"r");
	for line in GeometryFileId.readlines():

		ParList = re.split('\s*;\s*|\s*=\s*|\s*#\s*|\s*\(\s*|\s*\)\s*|\s+|\s*,\s*|\s*;\s*|',line);
		Command = ParList[0] + "_" + ParList[1];

		NumTokens = len(ParList);

		# The command is add node command
		if(Command=="add_node"):

			# print ParList;
			node = Node();

			for TokenNo in range(0,NumTokens):
				token = ParList[TokenNo];
				if(token=="node"):
					TokenNo = TokenNo+1;
					token = ParList[TokenNo];
					node.Id = int(token);
				if(token=="at"):
					TokenNo = TokenNo+1; token = ParList[TokenNo];
					node.Xcord = float(token.split('*')[0]);
					TokenNo = TokenNo+1; token = ParList[TokenNo];
					node.Ycord = float(token.split('*')[0]);
					TokenNo = TokenNo+1; token = ParList[TokenNo];
					node.Zcord = float(token.split('*')[0]);

			if node.Id in NodeList:
				if(NodeList[node.Id].Id == 0):
					NodeList[node.Id] = node;
					NumNodes = NumNodes + 1;
					X_Coordinate.append(node.Xcord);
					Y_Coordinate.append(node.Ycord);
					Z_Coordinate.append(node.Zcord);
					DRM_Nodes = np.append(DRM_Nodes,node.Id);
				else:
					print "\nWARNING:: [Generate_DRM]:: Node No " + str(node.Id) + "allready initialized Ignoring IT!! "; 		

	GeometryFileId.close();

	print "\n[Generate_DRM]:: Total Number of DRM Nodes Initialized are  " + str (NumNodes);
	if(NumNodes!=len(NodeList)):
		print "\nERROR:: [Generate_DRM]:: Only " + str (NumNodes) + "of " + str (len(NodeList)) + " were found and initialized" ;
		print "\nABORTING!! " ;
		exit();

	max_X_Coordinate = max(X_Coordinate);
	min_X_Coordinate = min(X_Coordinate);

	max_Y_Coordinate = max(Y_Coordinate);
	min_Y_Coordinate = min(Y_Coordinate);

	max_Z_Coordinate = max(Z_Coordinate);
	min_Z_Coordinate = min(Z_Coordinate);


	LowerXBound = min_X_Coordinate+WidthX;
	UpperXBound = max_X_Coordinate-WidthX;

	LowerYBound = min_Y_Coordinate+WidthY;
	UpperYBound = max_Y_Coordinate-WidthY;

	LowerZBound = min_Z_Coordinate+WidthZ;
	UpperZBound = max_Z_Coordinate;

	print "\n[Generate_DRM]:: DRM Inner Boundary Bounds are ";
	print "\t \t " + str(LowerXBound) + " < x < " + str(UpperXBound);
	print "\t \t " + str(LowerYBound) + " < y < " + str(UpperYBound);
	print "\t \t " + str(LowerZBound) + " < z < " + str(UpperZBound);

	print "\n[Generate_DRM]:: DRM Outer Boundary Bounds are "; 
	print "\t \t " + str(min_X_Coordinate) + " < x < " + str(max_X_Coordinate);
	print "\t \t " + str(min_Y_Coordinate) + " < y < " + str(max_Y_Coordinate);
	print "\t \t " + str(min_Z_Coordinate) + " < z < " + str(max_Z_Coordinate);


	# now iterate over all the nodes and fill interior and exterior node flags
	InteriorX=[]; ExteriorX=[];
	InteriorY=[]; ExteriorY=[];
	InteriorZ=[]; ExteriorZ=[];

	for i in DRM_Nodes:
		result = 1;
		NodeObj = NodeList[i];
		coord = NodeObj.Xcord;
		result = check(coord,LowerXBound,UpperXBound,Tol);
		coord = NodeObj.Ycord;
		result = result * check(coord,LowerYBound,UpperYBound,Tol);
		coord = NodeObj.Zcord;
		result = result * check(coord,LowerZBound,UpperZBound,Tol);
		if(result==1):
			NodeObj.Flag = 1;
			NumInteriorNodes = NumInteriorNodes +1;
			InteriorX.append(NodeObj.Xcord); InteriorY.append(NodeObj.Ycord);  InteriorZ.append(NodeObj.Zcord);
			DRM_Whether_Boundary_Node = np.append(DRM_Whether_Boundary_Node,1);
		else:
			ExteriorX.append(NodeObj.Xcord); ExteriorY.append(NodeObj.Ycord);  ExteriorZ.append(NodeObj.Zcord);
			DRM_Whether_Boundary_Node = np.append(DRM_Whether_Boundary_Node,0);
		

	print "\n \n[Generate_DRM]:: Number of Interior Nodes Found are " + str(NumInteriorNodes) ;
	NumExteriorNodes = NumNodes-NumInteriorNodes;
	print "\n \n[Generate_DRM]:: Number of Boundary Nodes then would be " + str(NumExteriorNodes) ;


	print "\n \n[Generate_DRM]:: Rendering DRM Layer ";
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(InteriorX, InteriorY, InteriorZ,c='r',marker='o',label='Interior Nodes');
	ax.scatter(ExteriorX, ExteriorY, ExteriorZ,c='k',marker='*',label='Exterior Nodes');
	ax.set_xlabel('X Label');
	ax.set_ylabel('Y Label');
	ax.set_zlabel('Z Label');

	# plt.show();
	plt.savefig(MotionName+'DRM_Layer.pdf');


	print "\n[Generate_DRM]:: Generating DRM Input File";


	DRMFileName = OutputPath + MotionName + ".drminput";
	fileId= h5py.File(DRMFileName, "w");

	# write drm layer data 
	datasetID = fileId.create_dataset("Elements", data=DRM_Elements);
	datasetID = fileId.create_dataset("DRM Nodes", data=DRM_Nodes);
	datasetID = fileId.create_dataset("Is Boundary Node", data=DRM_Whether_Boundary_Node);
	datasetID = fileId.create_dataset("Number of Boundary Nodes", data=NumInteriorNodes);
	datasetID = fileId.create_dataset("Number of Exterior Nodes", data=NumExteriorNodes);


	# generating acceleration and displacement field 
	TimeStep = 0.01;
	TotalTime = 1;
	file = "Field";

	Response     = raw_input("Do you want to generate Acceleration and Displacement field (Yes/no):: ");
	if( Response == 'Y' or Response == 'y' or Response == 'Yes' or Response == 'yes'):
		TimeStep     = float(raw_input("Enter time step  [s]:: "));
		TotalTime    = float(raw_input("Enter total time [s]:: "));
		message      = "Enter python file that would take x,y,z coordinate, time and  \nreturn displacement and acceleration in S.I. Units. \n"
		message      = message + "The file should have the getField(x,y,z,t) function as defined below. \n "
		message      = message + "\n---------------------------------------------------------------------------------------\n"
		message      = message + "displacement , acceleration  = getField(x,y,z,t)  \n "
		message      = message + " displacement = [u_x, u_y, u_z] \n"
		message      = message + " acceleration = [a_x, a_y, a_z] \n"
		message      = message + "--------------------------------------------------------------------------------------\n"
		message      = message + "\n Enter the python file :: "
		file     = raw_input(message);

		dir_path = os.path.dirname(os.path.realpath(file))
		sys.path.append(dir_path)

		filepath = os.path.realpath(file) +".py"

		if(not(os.path.exists(filepath)) or not(os.path.isfile(filepath))):
			print "ERROR:: File does not Exist"
			print "ABORTING!!"
			exit();

		#importing the module
		module = importlib.import_module(file, package=None);


		NumTime = int(TotalTime/TimeStep)+1;

		AccelerationId = fileId.create_dataset("Accelerations", (NumNodes*3, NumTime), chunks=(1,NumTime));
		DisplacementId = fileId.create_dataset("Displacements", (NumNodes*3, NumTime), chunks=(1,NumTime));
		DRM_Time       = np.empty((0),dtype=np.double);

		for i in range(0,NumTime):
			t = i*TimeStep;
			DRM_Time = np.append(DRM_Time,t);

		# writing time data 
		datasetID = fileId.create_dataset("Time", data=DRM_Time);

		# print DRM_Time

		DRM_Acceleration = np.empty((0),dtype=np.double);
		DRM_Displacement = np.empty((0),dtype=np.double);

		TestingSteps = TestNodeNum;

		NodeNo = 0;
		for j in DRM_Nodes:
			NodeObj = NodeList[j];
			x = NodeObj.Xcord*GF_Unit_To_SI_Unit;
			y = NodeObj.Ycord*GF_Unit_To_SI_Unit;
			z = NodeObj.Zcord*GF_Unit_To_SI_Unit;
			disp, acc = module.getField(NodeObj.Id,x,y,z,DRM_Time);
			DRM_Displacement = disp;
			DRM_Acceleration = acc;

			DisplacementId[3*NodeNo,:] = DRM_Displacement[0][:];
			DisplacementId[3*NodeNo+1,:] = DRM_Displacement[1][:];
			DisplacementId[3*NodeNo+2,:] = DRM_Displacement[2][:];
			AccelerationId[3*NodeNo,:] = DRM_Acceleration[0][:];
			AccelerationId[3*NodeNo+1,:] = DRM_Acceleration[1][:];
			AccelerationId[3*NodeNo+2,:] = DRM_Acceleration[2][:];

			NodeNo = NodeNo+1;

			if(TestNodeNum is not None):
				if(NodeNo==TestingSteps):
					break

			print "\n[Generate_DRM]:: Node No [ " + str(NodeNo) + " / " + str(NumNodes) + " ] completed .."

		print "\n[Generate_DRM]:: DRM Input file generated with Displacement and Acceleration Field";

	else:
		print "\n[Generate_DRM]:: DRM Input file generated without displacement and acceleration field";



