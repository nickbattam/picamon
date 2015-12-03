TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = Camera
# Camera.dbd will be created and installed
DBD += Camera.dbd

# Camera.dbd will be made up from these files:
Camera_DBD += base.dbd

# Include dbd files from all support applications:
Camera_DBD += asub.dbd
Camera_DBD += asyn.dbd
Camera_DBD += drvAsynIPPort.dbd
Camera_DBD += busySupport.dbd
Camera_DBD += ADSupport.dbd
Camera_DBD += NDPluginSupport.dbd
Camera_DBD += prosilicaSupport.dbd
Camera_DBD += asSupport.dbd
Camera_DBD += adPythonPlugin.dbd
Camera_DBD += simDetectorSupport.dbd

# Add all the support libraries needed by this IOC
Camera_LIBS += simDetector
Camera_LIBS += prosilica
Camera_LIBS += asyn
Camera_LIBS += autosave
Camera_LIBS += NDPlugin ADBase netCDF calc busy sscan autosave NDFileMagick GraphicsMagick++ GraphicsMagickWand GraphicsMagick PvAPI NeXus hdf5 sz tiff jpeg z
Camera_LIBS += seq pv
Camera_LIBS += adPython

Camera_SYS_LIBS += gomp X11 xml2 png12 bz2 Xext freetype
Camera_SYS_LIBS += opencv_calib3d opencv_core opencv_features2d
Camera_SYS_LIBS += opencv_flann opencv_hal opencv_highgui 
Camera_SYS_LIBS += opencv_imgcodecs opencv_imgproc opencv_ml opencv_objdetect
Camera_SYS_LIBS += opencv_photo opencv_shape opencv_stitching opencv_superres
Camera_SYS_LIBS += opencv_video opencv_videoio opencv_videostab

# Camera_registerRecordDeviceDriver.cpp derives from Camera.dbd
Camera_SRCS += Camera_registerRecordDeviceDriver.cpp
Camera_SRCS += camera.c
Camera_SRCS += findCentre.c
Camera_SRCS += rotateProfile.c

# Build any sequencer code
#Camera_SRCS += xxxx.st

# Build the main IOC entry point on workstation OSs.
Camera_SRCS_DEFAULT += CameraMain.cpp

# Finally link to the EPICS Base libraries
Camera_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

