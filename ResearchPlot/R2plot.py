#!/usr/bin/env python

"""Python Script To generate plots for research publication 
"""

__author__ = "Sumeet K. Sinha"
__credits__ = ["Hexiang Wang"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Sumeet K. Sinha"
__email__ = "sumeet.kumar507@gmail.com"


import matplotlib.pyplot as plt
from matplotlib import pylab
import matplotlib
from matplotlib.ticker import AutoMinorLocator
import numpy as np 

def R2plot(FontSize=26,LineWidth=2,LegendSize='small',X1=np.array([1,2,3,5]),Y1=np.array([1,2,2,5]),X2=np.array([1,5,1,5]),Y2=np.array([1,0,3,3]),Colour='k',Legend=['l'],Xlabel='xlabel',Ylabel='ylabel',NumXticks=5,NumYticks=4,FigName='RplotFigure.pdf',XlimMin=None,XlimMax=None,YlimMin=None,YlimMax=None,Xlog=None,Ylog=None,Alpha=1):

	# MatPlotlib
	import matplotlib
	matplotlib.use('Agg')

	import matplotlib.pyplot as plt

	from matplotlib import pylab
	
	from matplotlib.ticker import AutoMinorLocator
	import numpy as np 







	font = {'family' : 'arial', 'weight' : 'normal', 'size'   : FontSize}

	matplotlib.rc('font', **font)
	matplotlib.rc('lines', linewidth=LineWidth);

	# print(plt.style.available)
	plt.style.use('seaborn-colorblind')

	# plt.rc('legend',fontsize=18)
	plt.rc('legend',fontsize=LegendSize) # using a named size

	fig=plt.figure(figsize=(6,4))

	NumPlots =1; 
	Length   = X1.shape[0];

	index=0;

	for i in range(0,NumPlots):

		x = np.zeros(Length,dtype=np.double);
		y = np.zeros(Length,dtype=np.double);
		for j in range(0,Length):
			x[j]=X1[j];
			y[j]=Y1[j];

		plt.plot(x,y,color=Colour[index],label=Legend[index],alpha=Alpha)
		index=index+1;


	NumPlots = 1; 
	Length   = X2.shape[0];		
	
	for i in range(0,NumPlots):

		x = np.zeros(Length,dtype=np.double);
		y = np.zeros(Length,dtype=np.double);
		for j in range(0,Length):
			x[j]=X2[j];
			y[j]=Y2[j];

		plt.plot(x,y,color=Colour[index],label=Legend[index],alpha=Alpha)


	ax = plt.gca()
	ax.set_xlabel(Xlabel)
	ax.set_ylabel(Ylabel)

	if(Xlog==True):
		ax.set_xscale('log');
	if(Ylog==True):
		ax.set_yscale('log');	

	xmin, xmax = plt.xlim();
	ymin, ymax = plt.ylim();

	ApplyXlim=False;
	ApplyYlim=False;

	if(XlimMin!=None):
		xmin=XlimMin;
		ApplyXlim=True;
	if(XlimMax!=None):
		xmax=XlimMax;
		ApplyXlim=True;	
	if(YlimMin!=None):
		ymin=YlimMin;
		ApplyYlim=True;	
	if(YlimMax!=None):
		ymax=YlimMax;
		ApplyYlim=True;	

	if(ApplyXlim==True):
		plt.xlim(xmin, xmax);
	if(ApplyYlim==True):
		plt.ylim(ymin, ymax);	

	# Shrink current axis's height by 10% on the bottom
	box = ax.get_position()
	ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

	# Put a legend below current axis
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=10,frameon=False)


	# ax.legend(['Line Up', 'Line Down'],frameon=False)
	minorLocator = AutoMinorLocator()
	# ax.xaxis.set_minor_locator(minorLocator)
	# ax.yaxis.set_minor_locator(minorLocator)

	fig = plt.gcf()

	ax.autoscale_view()
	if(Xlog==None):
		ax.locator_params(nbins=NumXticks, axis='x')
	if(Ylog==None):
		ax.locator_params(nbins=NumYticks, axis='y')

	# plt.tick_params(which='both', width=2)
	# plt.tick_params(which='major', length=7)
	# plt.tick_params(which='minor', length=4)

	fig.savefig(FigName, transparent=True, bbox_inches='tight',  pad_inches=0)


# # # ####### dis fft response ##########################################################

# NumSteps_1= 687;
# NumSteps_2= 10321;

# X1 = np.zeros([NumSteps_1,1],dtype=np.double);
# Y1  = np.zeros([NumSteps_1,1],dtype=np.double);

# X2 = np.zeros([NumSteps_2,1],dtype=np.double);
# Y2  = np.zeros([NumSteps_2,1],dtype=np.double);

# Legend = ['free field','SW4 model'];
# Colour = ["r", "k"];
# Xlabel = "Frequency [Hz]";
# Ylabel = r'FFT $U_x$ [m]';
# FileName = "free_field_ux_frequency.pdf"


# XLFileName = "SMR_analysis.xlsx";
# XLSheetName = "free_field_model";
# XLStartRow=3;
# XLEndRow=NumSteps_1+XLStartRow-1;
# XLScaleFactor = 1.0;


# X1 = GetExcellData(XLFileName,XLSheetName,"B",XLStartRow,XLEndRow,XLScaleFactor);
# Y1= GetExcellData(XLFileName,XLSheetName,"J",XLStartRow,XLEndRow,XLScaleFactor);

# XLEndRow=NumSteps_2+XLStartRow-1;

# X2 = GetExcellData(XLFileName,XLSheetName,"R",XLStartRow,XLEndRow,XLScaleFactor);
# Y2= GetExcellData(XLFileName,XLSheetName,"Y",XLStartRow,XLEndRow,XLScaleFactor);


# # Rplot(FontSize,LineWidth,LegendSize,X1,Y1,X2,Y2,Colour,Legend,Xlabel,Ylabel,NumXticks,NumYticks,FigName,XlimMin,XlimMax,YlimMin,YlimMax,Xlog,Ylog):


# Rplot(26,2,'small',X1,Y1,X2,Y2,Colour,Legend,Xlabel,Ylabel,5,4,FileName,0,20,None,None,None,True)

