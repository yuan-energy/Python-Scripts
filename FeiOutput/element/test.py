from eleFile     import *
from eleGauss    import *
from eleOutpt   import *
from eleInfo     import *
from ele         import *

SequentialFeioutputFilename = '../Input_Files/NPPModel_Self_Weight_Check_Model.h5.feioutput';
ParallelFeioutputFileName   = '../Input_Files/NPPModel_Self_Weight.h5.feioutput';

# testing eleFile 
print eleFile(ParallelFeioutputFileName,30926);
print eleFile(SequentialFeioutputFilename,30926);

# # testing eleOutput
print eleOutpt(ParallelFeioutputFileName,30926);
print eleRelOutpt(ParallelFeioutputFileName,30926);
print eleGauss(SequentialFeioutputFilename,30926);
print eleRelGauss(SequentialFeioutputFilename,30926);

# # testing eleInfo
print eleInfo(ParallelFeioutputFileName,30926);
eleInfo(SequentialFeioutputFilename,30926);

# # testing ele class
elel1 =  ele(ParallelFeioutputFileName,30926);
print elel1.Gauss()
print elel1.Outpt()
ele(SequentialFeioutputFilename,30926);
