__author__ = "Sumeet K. Sinha"
__credits__ = [""]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Sumeet K. Sinha"
__email__ = "sumeet.kumar507@gmail.com"


import numpy as np;
from openpyxl import *;
import os.path;
import os;
from openpyxl.chart import ScatterChart, Reference, Series


def col2num(col):
	""" Changes Column Name to Column Number  """
	import string;
	num = 0;
	for c in col:
		if c in string.ascii_letters:
			num = num * 26 + (ord(c.upper()) - ord('A')) + 1
	return num


def ReadXLS(FileName,SheetName,StartRow,EndRow,StartColumn,EndColumn,ScaleFactor=1.0):
	""" Reads data in EXCELL for a given sheet and range """

	StartColumn = col2num(StartColumn);
	EndColumn   = col2num(EndColumn);

	WorkBookName = FileName;
	Data  = np.zeros([EndRow-StartRow+1,EndColumn-StartColumn+1],dtype=np.double);
	wb = Workbook();
	wb = load_workbook(WorkBookName,read_only=True,data_only=True,keep_vba=True);
	ws = wb[SheetName];

	StartRow=StartRow-1;
	EndRow=EndRow-1;
	StartColumn=StartColumn-1;
	EndColumn=EndColumn-1;

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
			# print "row_number " + str(row_number)
			column_number = 0;
			for cell in row:
				if(column_number<StartColumn):
					column_number = column_number + 1;
					continue;
				elif (column_number>EndColumn):
					break;
				else:
					cellVal = cell.value;
					# print "column_number " + str(column_number);
					if(cellVal is not None ):
						data  = float(cellVal)*ScaleFactor;
						Data[row_number-StartRow][column_number-StartColumn] = data;

				column_number = column_number + 1;
		row_number=row_number+1;
	################

	return Data;

