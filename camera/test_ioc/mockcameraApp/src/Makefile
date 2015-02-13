TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = mockcamera
# mockcamera.dbd will be created and installed
DBD += mockcamera.dbd

# mockcamera.dbd will be made up from these files:
mockcamera_DBD += base.dbd

# Include dbd files from all support applications:
#mockcamera_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
#mockcamera_LIBS += xxx

# mockcamera_registerRecordDeviceDriver.cpp derives from mockcamera.dbd
mockcamera_SRCS += mockcamera_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
mockcamera_SRCS_DEFAULT += mockcameraMain.cpp
mockcamera_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#mockcamera_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
mockcamera_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

