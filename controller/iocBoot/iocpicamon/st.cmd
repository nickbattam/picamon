#!../../bin/linux-x86_64/picamon

< envPaths

cd ${TOP}

## Register all support components
dbLoadDatabase "dbd/picamon.dbd"
picamon_registerRecordDeviceDriver pdbbase

## Load record instances

cd ${TOP}/iocBoot/${IOC}
dbLoadTemplate "general.substitutions"
dbLoadTemplate "monitor.substitutions"

iocInit

