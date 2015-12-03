This contains a camera simulator that creates a 400 x 400 simulated image.
This assumes you have the following installed:
-EPICS base 3.14.12.3
-AreaDetector R1-9-1

To run the simulator, simply go the simulator director and type 'make' to build the code.
Then run the st.cmd script. This will run the IOC and broadcast the set of camera related PVs using the prefix X2-CAM.

image array is available @ X2-CAM:image1:ArrayData
dimensions are available @ X2-CAM:cam1:SizeX and X2-CAM:cam1:SizeY



