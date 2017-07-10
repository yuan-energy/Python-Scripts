
#######################################################################################
#                                                                                     #
#                               pvESSI Camera                                         #
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  #
#                                                                                     #
#  GITHUB:: https://github.com/SumeetSinha/REAL-ESSI_Utility_Tools                    #
#                                                                                     #
#  Sumeet Kumar Sinha (April,2017)                                                    #
#  Computational Geomechanics Group                                                   #
#  University of California, Davis                                                    #
#  s u m e e t k s i n h a . c o m                                                    #
####################################################################################### 

from paraview.simple import *
LoadPlugin("libpvESSI.so",ns=globals());
from paraview.simple import *

def ResetSession():
    pxm = servermanager.ProxyManager();
    pxm.UnRegisterProxies();
    del pxm;
    Disconnect();
    Connect();

# ResetSession();
# ESSI_Output = pvESSI(FileName='/home/sumeet/sumeet.kumar507@gmail.com/git/pvESSI/Examples/ShearBox_Sequential.feioutput');

# # get animation scene
# animationScene1 = GetAnimationScene();

# # update animation scene based on data timesteps
# animationScene1.UpdateAnimationUsingDataTimeSteps();

# # get active view
# renderView1 = GetActiveViewOrCreate('RenderView');
# # uncomment following to set a specific view size
# # renderView1.ViewSize = [2405, 1879]

# # reset view to fit data
# renderView1.ResetCamera();

# # create a new 'Warp By Vector'
# warpByVector1 = WarpByVector(Input=ESSI_Output);
# warpByVector1.Vectors = ['POINTS', 'Generalized_Displacements'];
# warpByVector1.ScaleFactor = 50.37827622736076;

# # show data in view
# warpByVector1Display = Show(warpByVector1, renderView1)

# # set scalar coloring
# ColorBy(warpByVector1Display, ('POINTS', 'Generalized_Displacements'));

# # rescale color and/or opacity maps used to include current data range
# warpByVector1Display.RescaleTransferFunctionToDataRange(True, False);

# # show color bar/color legend
# warpByVector1Display.SetScalarBarVisibility(renderView1, True);

# #Show()
# #Render()
# #viewLayout = GetLayout()
# # save screenshot
# SaveScreenshot('/home/sumeet/sumeet.kumar507@gmail.com/git/REAL-ESSI_Utility_Tools/pvESSI_Camera/filename.png')

import time
 
#read a vtp
reader = pvESSI(FileName='/home/sumeet/sumeet.kumar507@gmail.com/git/pvESSI/Examples/ShearBox_Sequential.feioutput');

 
#position camera
view = GetActiveView()
if not view:
    # When using the ParaView UI, the View will be present, not otherwise.
    view = CreateRenderView()
view.CameraViewUp = [0, 0, 1]
view.CameraFocalPoint = [0, 0, 0]
view.CameraViewAngle = 45
view.CameraPosition = [5,0,0]
 
#draw the object
Show()
 
#set the background color
view.Background = [1,1,1]  #white
 
#set image size
view.ViewSize = [200, 300] #[width, height]
 
dp = GetDisplayProperties()
 
#set point color
dp.AmbientColor = [1, 0, 0] #red
 
#set surface color
dp.DiffuseColor = [0, 1, 0] #blue
 
#set point size
dp.PointSize = 2
 
#set representation
dp.Representation = "Surface"
 
Render()
 
#save screenshot
WriteImage("/home/sumeet/sumeet.kumar507@gmail.com/git/REAL-ESSI_Utility_Tools/pvESSI_Camera/filename.png")

# ResetSession();
