

SequentialFeioutputFilename = 'Beam_Axial_Load.h5.feioutput';
ParallelFeioutputFileName = 'NPPModel_DRM_Motion.h5.feioutput';


Sequential = RealESSI(SequentialFeioutputFilename);
Parallel   = RealESSI(ParallelFeioutputFileName);
print Sequential;
print Parallel;





