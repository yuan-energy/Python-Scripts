#!/usr/bin/env python

"""Python Script To generate plots for research publication 
"""

__author__ = "Sumeet K. Sinha"
__credits__ = [""]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Sumeet K. Sinha"
__email__ = "sumeet.kumar507@gmail.com"


import matplotlib.pyplot as plt
from matplotlib import pylab
import matplotlib
from matplotlib.ticker import AutoMinorLocator
import numpy as np 



def Rplot(FontSize=26,LineWidth=2,LegendSize='small',X=np.array([1,2,3,5]),Y=[1,4,2,5],Colour='k',Legend=['l'],Xlabel='xlabel',Ylabel='ylabel',NumXticks=5,NumYticks=4,FigName='RplotFigure.pdf',XlimMin=None,XlimMax=None,YlimMin=None,YlimMax=None,Xlog=None,Ylog=None,Alpha=1):
	""" Scrip that is used to generate publication figures 

	Parameters::
		- FontSize  : size of font
		- LinewWidth: width of line
		- LegendSize: font size of legend
		- X			: Data array X
		- Y			: Data array Y
		- Colour 	: colour list for legend
		- Lenend 	: legend list
		- Xlabel	: xlabel 
		- Ylabel	: ylabel
		- NumXticks : num ticks in x axis
		- NumYticks : num ticks in y axis
		- FigName   : figure name
		- XlimMin   : minimum x axis value
		- XlimMax	: maximum x axis value
		- YlimMin   : minimum y axis value
		- YlimMax	: maximum y axis value
		- Xlog 		: whether x axis in log
		- Ylog 		: whether y axis on log
		- alpha     : transparency level 

	"""

	font = {'family' : 'arial', 'weight' : 'normal', 'size'   : FontSize}

	matplotlib.rc('font', **font)
	matplotlib.rc('lines', linewidth=LineWidth);

	# print(plt.style.available)
	plt.style.use('seaborn-colorblind')

	# plt.rc('legend',fontsize=18)
	plt.rc('legend',fontsize=LegendSize) # using a named size

	fig=plt.figure(figsize=(6,4))

	if(len(X.shape)==1):
		NumPlots=1;
	else:
		NumPlots = X.shape[1]; 


	if(NumPlots==1):
		plt.plot(X[:],Y[:],color=Colour[0],alpha=Alpha)
	else:
		for i in range(0,NumPlots):
			plt.plot(X[:,i],Y[:,i],color=Colour[i],label=Legend[i],alpha=Alpha)

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
		# print ymin
		# print ymax;
		plt.ylim(ymin, ymax);	

	# Shrink current axis's height by 10% on the bottom
	box = ax.get_position()
	ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

	# Put a legend below current axis
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=10,frameon=False)


	# ax.legend(['Line Up', 'Line Down'],frameon=False)
	# minorLocator = AutoMinorLocator()
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

	fig.savefig(FigName, transparent=True, bbox_inches='tight', pad_inches=0)

