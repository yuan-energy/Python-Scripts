from nodeFile import *
from nodeDisp import *
from nodeDof  import *
from nodeInfo import *
from node import *

SequentialFeioutputFilename = '../Input_Files/NPPModel_Self_Weight_Check_Model.h5.feioutput';
ParallelFeioutputFileName   = '../Input_Files/NPPModel_Self_Weight.h5.feioutput';

# # testing nodeFile 
# print nodeFile(ParallelFeioutputFileName,30926);
# print nodeFile(SequentialFeioutputFilename,30926);

# # testing nodeDisp
# print nodeDisp(ParallelFeioutputFileName,30926);
# print nodeRelDisp(ParallelFeioutputFileName,30926,1);
# print nodeDof(SequentialFeioutputFilename,30926);
# print nodeRelDof(SequentialFeioutputFilename,30926,0);

# # testing nodeInfo
print nodeInfo(ParallelFeioutputFileName,30926);
# print nodeInfo(SequentialFeioutputFilename,30926);

# testing the node class 
node1 =  node(ParallelFeioutputFileName,30926);
node2 =  node(SequentialFeioutputFilename,30926);
print node2.Info()
