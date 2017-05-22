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

from Excell import *;

XLFileName = "./Input_Files/Test.xlsx";
XLSheetName = "Sheet1";
ExcellObject = Excell(XLFileName);
ExcellObject.createSheet(XLSheetName);

print ExcellObject;

x = np.array([1, 2, 3, 4])

ExcellObject.writeRow(XLSheetName,2,"A",x,["Sumeet"])
ExcellObject.writeRow(XLSheetName,3,"A",x,["Sumeet"])
ExcellObject.writeColumn(XLSheetName,2,"B",x,["Sumeet"])

# XLStartRow=7;
# XLEndRow=695;
# XLScaleFactor = 1.0;
# Gravity =9.81;
# Inv_Gravity =1/Gravity;
# X.createSheet('ki');

print ExcellObject.read(XLSheetName,2,3,"C","D");
print ExcellObject.reference(XLSheetName,2,3,"C","D");
# # print X.readRow(XLSheetName,8,"A","Z",XLScaleFactor);

# from openpyxl import Workbook
# from openpyxl.chart import (
#     ScatterChart,
#     Reference,
#     Series,
# )

# wb = Workbook()
# ws = wb.active

# rows = [
#     ['Size', 'Batch 1', 'Batch 2'],
#     [2, 40, 30],
#     [3, 40, 25],
#     [4, 50, 30],
#     [5, 30, 25],
#     [6, 25, 35],
#     [7, 20, 40],
# ]

# for row in rows:
#     ws.append(row)

# chart = ScatterChart()
# chart.title = "Scatter Chart"
# chart.style = 13
# chart.x_axis.title = 'Size'
# chart.y_axis.title = 'Percentage'

# xvalues = Reference(ws, min_col=1, min_row=2, max_row=7)
# for i in range(2, 4):
#     values = Reference(ws, min_col=i, min_row=1, max_row=7)
#     series = Series(values, xvalues, title_from_data=True)
#     chart.series.append(series)

# ws.add_chart(chart, "A10")

# wb.save("scatter.xlsx")