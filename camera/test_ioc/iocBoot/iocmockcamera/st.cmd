#!../../bin/linux-x86_64/mockcamera

## You may have to change mockcamera to something else
## everywhere it appears in this file

#< envPaths

## Register all support components
dbLoadDatabase("../../dbd/mockcamera.dbd",0,0)
mockcamera_registerRecordDeviceDriver(pdbbase) 

## Load record instances
dbLoadRecords("../../db/mockcamera.db","p=CAM1")

iocInit()

