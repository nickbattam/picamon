#!../../bin/linux-x86_64/picamon

## You may have to change picamon to something else
## everywhere it appears in this file

< envPaths

cd ${TOP}

## Register all support components
dbLoadDatabase "dbd/picamon.dbd"
picamon_registerRecordDeviceDriver pdbbase

## Load record instances
#dbLoadRecords("db/xxx.db","user=nickHost")
dbLoadRecords "db/general.db", "p=MON-CONTROL"
dbLoadRecords "db/monitor.db", "p=MON-CONTROL, monitor=PI1"
dbLoadRecords "db/monitor.db", "p=MON-CONTROL, monitor=PI2"


cd ${TOP}/iocBoot/${IOC}
iocInit

## Start any sequence programs
#seq sncxxx,"user=nickHost"
