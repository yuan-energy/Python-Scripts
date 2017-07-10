#!/usr/bin/env python


###########################################################################################################################
#                                                                                                                         #
#                               Visualize Coontact                                                                        #
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -                                      #
#                                                                                                                         #
#  GITHUB:: https://github.com/SumeetSinha/REAL-ESSI_Utility_Tools                                                        #
#                                                                                                                         #
#  Sumeet Kumar Sinha (January,2017)                                                                                      #
#  Computational Geomechanics Group                                                                                       #
#  University of California, Davis                                                                                        #
#  s u m e e t k s i n h a . c o m                                                                                        #
########################################################################################################################### 

import sys, os, os.path
import numpy as np
import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

filename = os.path.basename(sys.argv[1]).split('.')[0] 

f = h5py.File(sys.argv[1],  "r")

opfile = 'Contact_Analysis_of_'+ filename + '.tex'
outfile = open(opfile, 'w')
pageAry = []
def a_tex_file(title):
    global pageAry
    pageAry.append('\\documentclass[12pt]{article}\n')
    pageAry.append('\\usepackage{lmodern}\n')
    pageAry.append('\\usepackage{float} 							% for positioning figure \n')
    pageAry.append('\\usepackage{hyperref}\n')
    pageAry.append('\\usepackage{subfig}\n');
    pageAry.append('\\usepackage{graphicx}\n');
    pageAry.append('\\title{\\textbf{Contact Visualization} \\\\'+ filename.replace('_','\\_')+ '}\n')
    pageAry.append('\\author{Sumeet Kumar Sinha }\n')
    pageAry.append('\\begin{document}\n')
    pageAry.append('\\maketitle \\tableofcontents \n')
    return 1

a_tex_file("blunk");



Class_Tags = f['/Model/Elements/Class_Tags'];
Outputs = f['/Model/Elements/Outputs'];
Index_to_Outputs = f['/Model/Elements/Index_to_Outputs'];
Number_of_Time_Steps = f['Number_of_Time_Steps'][0];
time = f['time'];
Contact_Element = [];

for i in range(len(Class_Tags)):
	if(Class_Tags[i]==5015):
		Contact_Element.append(i);

Number_of_Contact_Elements = len(Contact_Element);

if(Number_of_Contact_Elements!=0):

	Full_3_D_Time_Axis = np.zeros((Number_of_Contact_Elements*Number_of_Time_Steps));
	Full_3_D_Contact_Element = np.zeros((Number_of_Contact_Elements*Number_of_Time_Steps));

	Normal_Force = np.zeros((Number_of_Contact_Elements*Number_of_Time_Steps));
	Tangential_Force_1 = np.zeros((Number_of_Contact_Elements*Number_of_Time_Steps));
	Tangential_Force_2 = np.zeros((Number_of_Contact_Elements*Number_of_Time_Steps));
	Relative_Normal_Disp = np.zeros((Number_of_Contact_Elements*Number_of_Time_Steps));
	Relative_Tangential_Disp_1 = np.zeros((Number_of_Contact_Elements*Number_of_Time_Steps));
	Relative_Tangential_Disp_2 = np.zeros((Number_of_Contact_Elements*Number_of_Time_Steps));

	os.system('mkdir ./images');
	element_index =0;

	for i in range(Number_of_Time_Steps):

		pageAry.append('\\section{Time Step ' + str(time[i]) +'}\n')

		if(time[i]==0):
			break;

		for j in range(Number_of_Contact_Elements):
			output_index = Index_to_Outputs[Contact_Element[j]];
			Normal_Force[element_index] = Outputs[output_index+5][i];
			Tangential_Force_1[element_index] = Outputs[output_index+3][i];
			Tangential_Force_2[element_index] = Outputs[output_index+4][i];
			Relative_Normal_Disp[element_index] = Outputs[output_index+2][i];
			Relative_Tangential_Disp_1[element_index] = Outputs[output_index][i];
			Relative_Tangential_Disp_2[element_index] = Outputs[output_index+1][i];
			Full_3_D_Time_Axis[element_index] = i;
			Full_3_D_Contact_Element[element_index] = Contact_Element[j];
			element_index = element_index+1;

			# Full_Normal_Force[j,i,i] = Outputs[output_index+5][i];

		plt.plot(Contact_Element,Tangential_Force_1[element_index-Number_of_Contact_Elements:element_index],'ro');
		plt.xlabel("Contact Element Number");
		plt.ylabel("Tangential_Force_1 ");
		plt.grid(True);
		plt.savefig('./images/Tangential_Force_1_'+str(i)+'.pdf');
		plt.clf();

		plt.plot(Contact_Element,Tangential_Force_2[element_index-Number_of_Contact_Elements:element_index],'ro');
		plt.xlabel("Contact Element Number");
		plt.ylabel("Tangential_Force_2 ");
		plt.grid(True);
		plt.savefig('./images/Tangential_Force_2_'+str(i)+'.pdf');
		plt.clf();

		plt.plot(Contact_Element,Normal_Force[element_index-Number_of_Contact_Elements:element_index],'ro');
		plt.xlabel("Contact Element Number");
		plt.ylabel("Normal_Force ");
		plt.grid(True);
		plt.savefig('./images/Normal_Force_'+str(i)+'.pdf');
		plt.clf();

		plt.plot(Contact_Element,Relative_Tangential_Disp_1[element_index-Number_of_Contact_Elements:element_index],'bo');
		plt.xlabel("Contact Element Number");
		plt.ylabel("Relative_Tangential_Disp_1 ");
		plt.grid(True);
		plt.savefig('./images/Relative_Tangential_Disp_1_'+str(i)+'.pdf');
		plt.clf();

		plt.plot(Contact_Element,Relative_Tangential_Disp_2[element_index-Number_of_Contact_Elements:element_index],'bo');
		plt.xlabel("Contact Element Number");
		plt.ylabel("Relative_Tangential_Disp_2 ");
		plt.grid(True);
		plt.savefig('./images/Relative_Tangential_Disp_2_'+str(i)+'.pdf');
		plt.clf();

		plt.plot(Contact_Element,Relative_Normal_Disp[element_index-Number_of_Contact_Elements:element_index],'bo');
		plt.xlabel("Contact Element Number");
		plt.ylabel("Relative_Normal_Disp ");
		plt.grid(True);
		plt.savefig('./images/Relative_Normal_Disp_'+str(i)+'.pdf');
		plt.clf();
		# plt.show()

		pageAry.append("\\begin{figure}[H]\n")
		pageAry.append("\t \\begin{center}\n")
		pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
		pageAry.append("\t \t {./images/Normal_Force_"+ str(i)+ ".pdf}}\n")
		pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
		pageAry.append("\t \t {./images/Relative_Normal_Disp_"+ str(i)+ ".pdf}} \\\\ \n")
		pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
		pageAry.append("\t \t {./images/Tangential_Force_1_"+ str(i)+ ".pdf}}\n")
		pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
		pageAry.append("\t \t {./images/Relative_Tangential_Disp_1_"+ str(i)+ ".pdf}} \\\\ \n")
		pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
		pageAry.append("\t \t {./images/Tangential_Force_2_"+ str(i)+ ".pdf}}\n")
		pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
		pageAry.append("\t \t {./images/Relative_Tangential_Disp_2_"+ str(i)+ ".pdf}}\n")
		pageAry.append("\t \\end{center}\n")
		pageAry.append("\t \\caption{\\label{Case_3_Monotonic_Loading_with_initial_gap}  Contact Element State at Time Step $ T = "+ str(time[i])+ " $}\n")
		pageAry.append("\\end{figure}\n")

	f.close();


	pageAry.append('\\section{All Time Steps Combined }\n')

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(Full_3_D_Time_Axis, Full_3_D_Contact_Element, Normal_Force, c='r', marker='o')
	ax.set_xlabel("Time Step  ");
	ax.set_ylabel("Contact Element Number");
	ax.set_zlabel('Normal_Force');
	plt.grid(True);
	plt.savefig('./images/All_Normal_Force.pdf');
	plt.clf();

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(Full_3_D_Time_Axis, Full_3_D_Contact_Element, Tangential_Force_1, c='r', marker='o')
	ax.set_xlabel("Time Step  ");
	ax.set_ylabel("Contact Element Number");
	ax.set_zlabel('Tangential_Force_1');
	plt.grid(True);
	plt.savefig('./images/All_Tangential_Force_1.pdf');
	plt.clf();

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(Full_3_D_Time_Axis, Full_3_D_Contact_Element, Tangential_Force_2, c='r', marker='o')
	ax.set_xlabel("Time Step  ");
	ax.set_ylabel("Contact Element Number");
	ax.set_zlabel('Tangential_Force_2');
	plt.grid(True);
	plt.savefig('./images/All_Tangential_Force_2.pdf');
	plt.clf();

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(Full_3_D_Time_Axis, Full_3_D_Contact_Element, Relative_Normal_Disp, c='b', marker='o')
	ax.set_xlabel("Time Step  ");
	ax.set_ylabel("Contact Element Number");
	ax.set_zlabel('Relative_Normal_Disp');
	plt.grid(True);
	plt.savefig('./images/All_Relative_Normal_Disp.pdf');
	plt.clf();

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(Full_3_D_Time_Axis, Full_3_D_Contact_Element, Relative_Tangential_Disp_1, c='b', marker='o')
	ax.set_xlabel("Time Step  ");
	ax.set_ylabel("Contact Element Number");
	ax.set_zlabel('Relative_Tangential_Disp_1');
	plt.grid(True);
	plt.savefig('./images/All_Relative_Tangential_Disp_1.pdf');
	plt.clf();

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(Full_3_D_Time_Axis, Full_3_D_Contact_Element, Relative_Tangential_Disp_2, c='b', marker='o')
	ax.set_xlabel("Time Step  ");
	ax.set_ylabel("Contact Element Number");
	ax.set_zlabel('Relative_Tangential_Disp_2');
	plt.grid(True);
	plt.savefig('./images/All_Relative_Tangential_Disp_2.pdf');
	plt.clf();

	pageAry.append("\\begin{figure}[H]\n")
	pageAry.append("\t \\begin{center}\n")
	pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
	pageAry.append("\t \t {./images/All_Normal_Force.pdf}}\n")
	pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
	pageAry.append("\t \t {./images/All_Relative_Normal_Disp.pdf}} \\\\ \n")
	pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
	pageAry.append("\t \t {./images/All_Tangential_Force_1.pdf}}\n")
	pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
	pageAry.append("\t \t {./images/All_Relative_Tangential_Disp_1.pdf}} \\\\ \n")
	pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
	pageAry.append("\t \t {./images/All_Tangential_Force_2.pdf}}\n")
	pageAry.append("\t \t \\subfloat{\includegraphics[width=0.5\\textwidth]\n")
	pageAry.append("\t \t {./images/All_Relative_Tangential_Disp_2.pdf}}\n")
	pageAry.append("\t \\end{center}\n")
	pageAry.append("\t \\caption{\\label{Case_3_Monotonic_Loading_with_initial_gap}  Contact Element State at all Time Steps } \n")
	pageAry.append("\\end{figure}\n")

pageAry.append('\\end{document}\n')

for i in pageAry:
    outfile.writelines(i)
outfile.close()
os.system('pdflatex '+ opfile)
os.system('pdflatex '+ opfile)
os.system('pdflatex '+ opfile)
os.system('pdflatex '+ opfile)
os.system('find Contact_Analysis_of_' + filename + '.* \! -name ' + 'Contact_Analysis_of_'+filename+'.pdf -delete')



# print Full_Normal_Force
