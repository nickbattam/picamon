TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = picamon
# picamon.dbd will be created and installed
DBD += picamon.dbd

# picamon.dbd will be made up from these files:
picamon_DBD += base.dbd

# Include dbd files from all support applications:
#picamon_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
#picamon_LIBS += xxx

# picamon_registerRecordDeviceDriver.cpp derives from picamon.dbd
picamon_SRCS += picamon_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
picamon_SRCS_DEFAULT += picamonMain.cpp
picamon_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#picamon_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
picamon_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

