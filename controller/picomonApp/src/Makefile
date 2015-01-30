TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = picomon
# picomon.dbd will be created and installed
DBD += picomon.dbd

# picomon.dbd will be made up from these files:
picomon_DBD += base.dbd

# Include dbd files from all support applications:
#picomon_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
#picomon_LIBS += xxx

# picomon_registerRecordDeviceDriver.cpp derives from picomon.dbd
picomon_SRCS += picomon_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
picomon_SRCS_DEFAULT += picomonMain.cpp
picomon_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#picomon_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
picomon_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

