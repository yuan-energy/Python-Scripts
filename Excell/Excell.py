#!/usr/bin/env python

"""Base Class which contains basic information for REAL ESSI Elements.

It contains Class Tag and Class Tag description  for each element in 
Real ESSI Simulator System.
"""

__author__ = "Sumeet K. Sinha"
__credits__ = [""]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Sumeet K. Sinha"
__email__ = "sumeet.kumar507@gmail.com"


import numpy as np;
from openpyxl import *;
import os.path;

class Excell:
	'It reads the microsoft excell file'

	FileName     = None;
	WorkBook     = None;
	WorkSheets   = None;

	def __str__(self):
		return "\
\n---------------------------------------\n\
Excell -> %s\n---------------------------------------\n\t\
WorkSheets:: %s\n\t\
" % (self.FileName,self.WorkSheets)

	def __init__ (self,inputFile):
		""" Define Excell class with output file

		Class Variables:
		FileName -- the hdf5.feioutput filename
		"""
		self.FileName = inputFile;
		self.__initialize();


	def __initialize(self):

		self.WorkBook = Workbook(write_only=True);
		if(os.path.exists(self.FileName)):
			self.WorkBook = load_workbook(self.FileName,read_only=True,data_only=True);
		else:
			self.WorkBook.save(self.FileName);
		self.WorkSheets = self.WorkBook.sheetnames;
		self.WorkBook = Workbook();
		return 

	def createSheet(self,SheetName):
		""" Create a Sheet in active workbook """
		self.WorkBook = Workbook(write_only=True);
		self.WorkBook = load_workbook(self.FileName);
		self.WorkBook.create_sheet(SheetName);
		self.WorkBook.save(self.FileName);



	# Changes Column Name to Column Number 
	def col2num(self,col):

		import string;
		num = 0;
		for c in col:
			if c in string.ascii_letters:
				num = num * 26 + (ord(c.upper()) - ord('A')) + 1
		return num


	# Gets the Excell data 
	def readColumn(self,SheetName,ColumnName,StartRow,EndRow,ScaleFactor=1.0):

		ColumnNumber = self.col2num(ColumnName);
		WorkBookName = self.FileName;
		Data  = np.zeros([EndRow-StartRow+1],dtype=np.double);
		wb = Workbook();
		wb = load_workbook(WorkBookName,read_only=True,data_only=True);
		ws = wb[SheetName];

		StartRow=StartRow-1;
		EndRow=EndRow-1;
		ColumnNumber=ColumnNumber-1;

		row_number = 0;
		column_number = 0;

		###### Read WorkSheets
		for row in ws.rows:
			if (row_number<StartRow):
				row_number=row_number+1;
				continue;
			elif (row_number>EndRow):
				break;
			else:
				column_number = 0;
				for cell in row:
					# print column_number
					if (column_number==ColumnNumber):
						cellVal = cell.value;
						if(cellVal is not None ):
							data  = float(cellVal)*ScaleFactor;
							Data[row_number-StartRow] = data;
						# else:
						# 	break;

					elif(column_number>ColumnNumber):
						break;
					column_number = column_number + 1;
			row_number=row_number+1;
		################

		return Data;

	# Gets the Excell data 
	def readRow(self,SheetName,RowNumber,StartColumn,EndColumn,ScaleFactor=1.0):

		StartColumnNumber = self.col2num(StartColumn);
		EndColumnNumber   = self.col2num(EndColumn);

		WorkBookName = self.FileName;
		Data  = np.zeros([EndColumnNumber-StartColumnNumber+1],dtype=np.double);
		wb = Workbook();
		wb = load_workbook(WorkBookName,read_only=True,data_only=True);
		ws = wb[SheetName];

		StartColumnNumber=StartColumnNumber-1;
		EndColumnNumber=EndColumnNumber-1;
		RowNumber=RowNumber-1;

		row_number = 0;
		column_number = 0;

		###### Read WorkSheets
		for row in ws.rows:
			if (row_number<RowNumber):
				row_number=row_number+1;
				continue;
			elif (row_number>RowNumber):
				break;
			else:
				column_number = 0;
				for cell in row:
					# print column_number
					if(column_number<StartColumnNumber):
						column_number = column_number + 1;
						continue;
					elif(column_number>EndColumnNumber):
						break;
					else:
						cellVal = cell.value;
						if(cellVal is not None ):
							data  = float(cell.value)*ScaleFactor;
							Data[column_number-StartColumnNumber] = data;
						# else:
						# 	break;

					column_number = column_number + 1;
			row_number=row_number+1;
		################

		return Data;

	# Gets the Excell data 
	def writeRow(self,SheetName,RowNumber,StartColumn,EndColumn,ScaleFactor=1.0):

		StartColumnNumber = self.col2num(StartColumn);
		EndColumnNumber   = self.col2num(EndColumn);

		WorkBookName = self.FileName;
		Data  = np.zeros([EndColumnNumber-StartColumnNumber+1],dtype=np.double);
		wb = Workbook();
		wb = load_workbook(WorkBookName,read_only=True,data_only=True);
		ws = wb[SheetName];

		StartColumnNumber=StartColumnNumber-1;
		EndColumnNumber=EndColumnNumber-1;
		RowNumber=RowNumber-1;

		row_number = 0;
		column_number = 0;

		###### Read WorkSheets
		for row in ws.rows:
			if (row_number<RowNumber):
				row_number=row_number+1;
				continue;
			elif (row_number>RowNumber):
				break;
			else:
				column_number = 0;
				for cell in row:
					# print column_number
					if(column_number<StartColumnNumber):
						column_number = column_number + 1;
						continue;
					elif(column_number>EndColumnNumber):
						break;
					else:
						cellVal = cell.value;
						if(cellVal is not None ):
							data  = float(cell.value)*ScaleFactor;
							Data[column_number-StartColumnNumber] = data;
						# else:
						# 	break;

					column_number = column_number + 1;
			row_number=row_number+1;
		################

		return Data;

	# Gets the Excell data 
	def writeColumn(self,SheetName,ColumnName,StartRow,EndRow,ScaleFactor=1.0):

		ColumnNumber = self.col2num(ColumnName);
		WorkBookName = self.FileName;
		Data  = np.zeros([EndRow-StartRow+1],dtype=np.double);
		wb = Workbook();
		wb = load_workbook(WorkBookName,read_only=True,data_only=True);
		ws = wb[SheetName];

		StartRow=StartRow-1;
		EndRow=EndRow-1;
		ColumnNumber=ColumnNumber-1;

		row_number = 0;
		column_number = 0;

		###### Read WorkSheets
		for row in ws.rows:
			if (row_number<StartRow):
				row_number=row_number+1;
				continue;
			elif (row_number>EndRow):
				break;
			else:
				column_number = 0;
				for cell in row:
					# print column_number
					if (column_number==ColumnNumber):
						cellVal = cell.value;
						if(cellVal is not None ):
							data  = float(cellVal)*ScaleFactor;
							Data[row_number-StartRow] = data;
						# else:
						# 	break;

					elif(column_number>ColumnNumber):
						break;
					column_number = column_number + 1;
			row_number=row_number+1;
		################

		return Data;

XLFileName = "Test2.xlsx";
XLSheetName = "Motion";
X = Excell(XLFileName);
print X;
XLStartRow=7;
XLEndRow=695;
XLScaleFactor = 1.0;
Gravity =9.81;
Inv_Gravity =1/Gravity;
X.createSheet('ki');

# print X.readColumn(XLSheetName,"A",XLStartRow,XLEndRow,XLScaleFactor);
# print X.readRow(XLSheetName,8,"A","Z",XLScaleFactor);