#!/bin/bash

echo Launching PiCaMon...
sleep 1

#load the EPICS environment
. /usr/local/epics/siteEnv

# launch python script
/home/pi/picamon/monitor/picamon.py --prefix D100X --name MONITOR1 --fullscreen True

# keep the terminal open  in case it crashes
read -n1 -rsp $'press any keep to close the terminal...\n'




