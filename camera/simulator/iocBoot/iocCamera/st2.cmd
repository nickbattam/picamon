#!../../bin/linux-x86_64/Camera

< envPaths

## Register all support components
dbLoadDatabase "${TOP}/dbd/Camera.dbd"
Camera_registerRecordDeviceDriver pdbbase

#-----------------------------------------------
# CAMERA SECTION
# Call the startup file for each camera

epicsEnvSet("PREFIX", "X1-CAM:")
epicsEnvSet("CAMID",  "192.168.42.105")
< st.cmd.camera

#-----------------------------------------------
# DATABASE SECTION
dbLoadRecords("${TOP}/db/CameraGeneric.db","CAMERA_NAME=X1-CAM, ARRAYSIZE=$(ARRAYSIZE)")
dbLoadRecords("${TOP}/db/CameraViewer.db","CAMERA_NAME=X1-CAM, XSIZE=$(XSIZE), YSIZE=$(YSIZE)")
dbLoadRecords("${TOP}/db/custom_centroid.db", "CAMERA_NAME=X1-CAM, SUFFIX=Centroid, ARRAYSIZE=$(ARRAYSIZE), XSIZE=$(XSIZE), YSIZE=$(YSIZE)")
dbLoadRecords("${TOP}/db/centroidSelect.db","CAMERA_NAME=X1-CAM, STATS=Stats1, ASUB=Centroid")
dbLoadRecords("${TOP}/db/centroidLock.db","CAMERA_NAME=X1-CAM")
dbLoadRecords("${TOP}/db/autoStreaming.db","CAMERA_NAME=X1-CAM")
dbLoadRecords("${TOP}/db/heartbeat.db","DEVICE=X1-CAM")

#-----------------------------------------------
# AUTOSAVE SECTION

# Configure autosave
set_requestfile_path("$(AREA_DETECTOR)/ADApp/Db")
set_requestfile_path("$(CALC)/calcApp/Db")
set_requestfile_path("$(SSCAN)/sscanApp/Db")
set_requestfile_path("$(MOTOR)/motorApp/Db")
set_requestfile_path("$(TOP)/autoSaveRestore")

set_savefile_path("/home/swdev/HiLASE/live/../autosave/cameras/X1-CAM")
set_pass0_restoreFile("single_setting2.sav")
set_pass1_restoreFile("single_setting2.sav")
set_pass1_restoreFile("centroid.sav")

#-----------------------------------------------

# Start the soft IOC
cd ${TOP}/iocBoot/${IOC}
iocInit

#-----------------------------------------------
# POST-BOOT SECTION

# save things every 5 seconds
create_monitor_set("single_setting.req", 5)
create_monitor_set("centroid.req", 5, "cam=X1-CAM, suffix=Centroid")

#-----------------------------------------------
# force some settings regardless of what autosave says

dbpf $(PREFIX)cam1:ArrayCallbacks 1
dbpf $(PREFIX)cam1:SizeX $(XSIZE)
dbpf $(PREFIX)cam1:SizeY $(YSIZE)

dbpf $(PREFIX)ROI1:NDArrayPort $(PREFIX)CAM
dbpf $(PREFIX)ROI1:EnableCallbacks 1
dbpf $(PREFIX)ROI1:SizeX $(XSIZE)
dbpf $(PREFIX)ROI1:SizeY $(YSIZE)

dbpf $(PREFIX)Trans1:EnableCallbacks 1

dbpf $(PREFIX)Stats1:NDArrayPort $(PREFIX)TRANS
dbpf $(PREFIX)Stats1:EnableCallbacks 1
dbpf $(PREFIX)Stats1:ComputeCentroid 1
dbpf $(PREFIX)Stats1:CentroidThreshold 10
dbpf $(PREFIX)Stats1:ComputeProfiles 1

dbpf $(PREFIX)image1:NDArrayPort $(PREFIX)OVER
dbpf $(PREFIX)image1:EnableCallbacks 1


dbpf $(PREFIX)image2:NDArrayPort $(PREFIX)TRANS
dbpf $(PREFIX)image2:EnableCallbacks 1

dbpf $(PREFIX)Over1:NDArrayPort $(PREFIX)TRANS
dbpf $(PREFIX)Over1:EnableCallbacks 1
dbpf $(PREFIX)Over1:NDArrayAddress 0
dbpf $(PREFIX)Over1:MinCallbackTime 0
dbpf $(PREFIX)Over1:BlockingCallbacks 0
dbpf $(PREFIX)Over1:1:DrawMode 1
dbpf $(PREFIX)Over1:1:PositionXLink.DOL "$(PREFIX)SOFT_REF_X CP MS"
dbpf $(PREFIX)Over1:1:PositionYLink.DOL "$(PREFIX)SOFT_REF_Y CP MS"
dbpf $(PREFIX)Over1:1:Red 100
dbpf $(PREFIX)Over1:1:Green 100
dbpf $(PREFIX)Over1:1:Blue 100
dbpf $(PREFIX)Over1:2:DrawMode 1
dbpf $(PREFIX)Over1:2:PositionXLink.DOL "$(PREFIX)SOFT_REF_X_PLUS CP MS"
dbpf $(PREFIX)Over1:2:PositionYLink.DOL "$(PREFIX)SOFT_REF_Y_PLUS CP MS"
dbpf $(PREFIX)Over1:2:Red 100
dbpf $(PREFIX)Over1:2:Green 100
dbpf $(PREFIX)Over1:2:Blue 100
dbpf $(PREFIX)Over1:3:DrawMode 1
dbpf $(PREFIX)Over1:3:PositionXLink.DOL "$(PREFIX)SOFT_REF_X_MINUS CP MS"
dbpf $(PREFIX)Over1:3:PositionYLink.DOL "$(PREFIX)SOFT_REF_Y_MINUS CP MS"
dbpf $(PREFIX)Over1:3:Red 100
dbpf $(PREFIX)Over1:3:Green 100
dbpf $(PREFIX)Over1:3:Blue 100
dbpf $(PREFIX)Over1:4:DrawMode 1
dbpf $(PREFIX)Over1:4:PositionXLink.DOL "$(PREFIX)Stats1:CursorX CP MS"
dbpf $(PREFIX)Over1:4:PositionYLink.DOL "$(PREFIX)Stats1:CursorY CP MS"
dbpf $(PREFIX)Over1:4:Red 100
dbpf $(PREFIX)Over1:4:Green 100
dbpf $(PREFIX)Over1:4:Blue 100
dbpf $(PREFIX)Over1:5:DrawMode 1
dbpf $(PREFIX)Over1:5:PositionXLink.DOL "$(PREFIX)PROF_X_PLUS CP MS"
dbpf $(PREFIX)Over1:5:PositionYLink.DOL "$(PREFIX)PROF_Y_PLUS CP MS"
dbpf $(PREFIX)Over1:5:Red 100
dbpf $(PREFIX)Over1:5:Green 100
dbpf $(PREFIX)Over1:5:Blue 100
dbpf $(PREFIX)Over1:6:DrawMode 1
dbpf $(PREFIX)Over1:6:PositionXLink.DOL "$(PREFIX)PROF_X_MINUS CP MS"
dbpf $(PREFIX)Over1:6:PositionYLink.DOL "$(PREFIX)PROF_Y_MINUS CP MS"
dbpf $(PREFIX)Over1:6:Red 100
dbpf $(PREFIX)Over1:6:Green 100
dbpf $(PREFIX)Over1:6:Blue 100
dbpf $(PREFIX)Over1:7:DrawMode 1
dbpf $(PREFIX)Over1:7:PositionXLink.DOL "$(PREFIX)RECT_X CP MS"
dbpf $(PREFIX)Over1:7:PositionYLink.DOL "$(PREFIX)RECT_Y CP MS"
dbpf $(PREFIX)Over1:7:Red 100
dbpf $(PREFIX)Over1:7:Green 100
dbpf $(PREFIX)Over1:7:Blue 100
dbpf $(PREFIX)Over1:8:DrawMode 1
dbpf $(PREFIX)Over1:8:PositionXLink.DOL "$(PREFIX)RECT_X_PLUS CP MS"
dbpf $(PREFIX)Over1:8:PositionYLink.DOL "$(PREFIX)RECT_Y_PLUS CP MS"
dbpf $(PREFIX)Over1:8:Red 100
dbpf $(PREFIX)Over1:8:Green 100
dbpf $(PREFIX)Over1:8:Blue 100
dbpf $(PREFIX)Over1:9:DrawMode 1
dbpf $(PREFIX)Over1:9:PositionXLink.DOL "$(PREFIX)RECT_X_MINUS CP MS"
dbpf $(PREFIX)Over1:9:PositionYLink.DOL "$(PREFIX)RECT_Y_MINUS CP MS"
dbpf $(PREFIX)Over1:9:Red 100
dbpf $(PREFIX)Over1:9:Green 100
dbpf $(PREFIX)Over1:9:Blue 100

dbpf $(PREFIX)COLOUR_MAP ColorSpectrum
dbpf X1-CAM:SIMULATION 1
dbpf X1-CAM:cam1:SimMode 1
dbpf X1-CAM:cam1:PeakVariation 8
dbpf X1-CAM:cam1:Noise 50
dbpf X1-CAM:cam1:GainX 50
dbpf X1-CAM:cam1:GainY 1
dbpf X1-CAM:cam1:Gain 1
dbpf X1-CAM:cam1:PeakNumX 1
dbpf X1-CAM:cam1:PeakNumY 1
dbpf X1-CAM:cam1:PeakStepX 100
dbpf X1-CAM:cam1:PeakStepY 100
dbpf X1-CAM:cam1:PeakWidthX 50
dbpf X1-CAM:cam1:PeakWidthY 50
dbpf X1-CAM:cam1:PeakStartX 300
dbpf X1-CAM:cam1:PeakStartY 300
