#!/bin/bash

set -e
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

if [ -z "$*" ]; then
    echo "no arguments supplied. 1:configfile 2:destination"
    exit 1
fi

# read config file
CONFIG=$(readlink -f $1)

# source directory is one level up from the script folder
SOURCE=$(readlink -f $DIR/..)
echo Source folder: $SOURCE

# create the destination folder if it does not exists
ROOT=$(readlink -f $2)
DESTINATION=$ROOT/cameras
echo Destination folder: $DESTINATION

if [ ! -d $DESTINATION ]; then
    echo "Specified destination directory does not exists. Will create it now."
    mkdir -p $DESTINATION
fi

# monitoring command file
monitoring_file=$DESTINATION/monitoring_camera.cmd
touch $monitoring_file
> $monitoring_file

# traffic light command file
traffic_light_file=$DESTINATION/traffic_light_camera.cmd
touch $traffic_light_file
> $traffic_light_file

# list of devices command file
devices_config_file=$DESTINATION/devices_camera.cmd
touch $devices_config_file
> $devices_config_file
devices=""

while read -a param ; do

    # skip empty line
    [[ -z ${param[0]} ]] && continue

    # skip line starting with #
    [[ ${param[0]} =~ ^#.* ]] && continue

    # get parameters from config file
    pv_name=${param[0]}
    ip_addr=${param[1]}
    xsize=${param[2]}
    ysize=${param[3]}
    asize=$(( $xsize * $ysize ))

    if [[ "$ip_addr" = "simulation" ]]; then
        echo "setting up" $pv_name "as a simulated camera feed"
        type=${param[4]}
    else
        echo "setting up" $pv_name "with IP address" $ip_addr
    fi

    #create autosave folder if it does not exist
    AUTOSAVE=$ROOT/../autosave/cameras/$pv_name
    if [ ! -d $AUTOSAVE ]; then
        echo "Autosave directory does not exist. Will create it now."
        mkdir -p $AUTOSAVE
    fi

    # copy files
    rsync -arvud --exclude=".svn*" $SOURCE/ $DESTINATION/$pv_name

    # set PV name
    find $DESTINATION/$pv_name -type f -exec sed -i "s/X2-CAM/$pv_name/g" {} +


    if [[ "$ip_addr" = "simulation" ]]; then
        # comment out camera driver
        sed -i -e "/prosilicaConfig/ s|prosilicaConfig|#prosilicaConfig|" $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd.camera
        sed -i -e "/prosilica.template/ s|dbLoadRecords|#dbLoadRecords|" $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd.camera

        echo dbpf $pv_name:SIMULATION 1 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
        echo dbpf $pv_name:cam1:SimMode 1 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
        echo dbpf $pv_name:cam1:PeakVariation $(shuf -i 3-10 -n 1) >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
        echo dbpf $pv_name:cam1:Noise $(shuf -i 3-20 -n 1) >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd

        if [[ "$type" = "square" ]];then
            echo dbpf $pv_name:cam1:GainX 1 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:GainY 1 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:Gain $(shuf -i 40-60 -n 1) >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakNumX 5 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakNumY 5 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakStepX 100 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakStepY 100 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakWidthX 50 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakWidthY 50 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakStartX $(shuf -i 200-$(( $xsize/2 )) -n 1) >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakStartY $(shuf -i 200-$(( $ysize/2 )) -n 1)>> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            fi

        if [[ "$type" = "gaussian" ]];then
            echo dbpf $pv_name:cam1:GainX $(shuf -i 8-20 -n 1) >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:GainY $(shuf -i 8-20 -n 1) >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:Gain 1 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakNumX 1 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakNumY 1 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakStepX 100 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakStepY 100 >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakWidthX $(shuf -i 100-150 -n 1) >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakWidthY $(shuf -i 100-150 -n 1) >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakStartX $(shuf -i 200-$(( $xsize/2 )) -n 1) >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            echo dbpf $pv_name:cam1:PeakStartY $(shuf -i 200-$(( $ysize/2 )) -n 1) >> $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
            fi

    else
        # comment out simulation driver
        sed -i -e "/simDetectorConfig/ s|simDetectorConfig|#simDetectorConfig|" $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd.camera
        sed -i -e "/simDetector.template/ s|dbLoadRecords|#dbLoadRecords|" $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd.camera
        # set IP address
        sed -i -e "/epicsEnvSet(\"CAMID\"/ s|[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}|$ip_addr|" $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd
    fi


    # set camera's sensor size
    sed -i -e "/epicsEnvSet(\"XSIZE\"/ s|[0-9]\+|$xsize|" $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd.camera
    sed -i -e "/epicsEnvSet(\"YSIZE\"/ s|[0-9]\+|$ysize|" $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd.camera
    sed -i -e "/epicsEnvSet(\"ARRAYSIZE\"/ s|[0-9]\+|$asize|" $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd.camera

    # set autosave path
    sed -i -e "/set_savefile_path(\"/ s|\$(TOP)/autoSaveRestore|$AUTOSAVE|" $DESTINATION/$pv_name/iocBoot/iocCamera/st.cmd

    # build code
    pushd $DESTINATION/$pv_name/ 
    make clean uninstall
    make
    popd

    # generate st.cmd commands for the monitoring IOC
    echo "dbLoadRecords(\"db/monitor_ioc.db\", \"DEVICE=MONITOR, NAME=$pv_name, IOC=$pv_name\")" >> $monitoring_file

    # generate st.cmd commands for the traffic light IOC
    echo "dbLoadRecords(\"db/traffic_light.db\",\"NAME=$pv_name\")" >> $traffic_light_file
    echo "dbLoadRecords(\"db/camera_adapter.db\",\"NAME=$pv_name, MONITOR=MONITOR\")" >> $traffic_light_file

    # make a list of PV names
    devices="$devices $pv_name"
    devices_count=$((devices_count+1))
    echo $devices_count

    # add to the list of IOCs to be launched
    echo $pv_name $DESTINATION/$pv_name/  >> $(readlink -f $DIR/../../../manage/process/iocBoot/iocprocess/iocs.conf)

done < $CONFIG

# add pv name to list of devices
echo "system \"caput -a -s DEVICES:CAMERAS" $devices_count $devices"\"" >> $devices_config_file

# add list of PV prefixes to config file used by Manager OPI
echo $devices >> $DIR/../../../manage/opi/pvs.conf

# deploy the CSS opi screens
> $SOURCE/../opi/pvs.conf
echo $devices >> $SOURCE/../opi/pvs.conf
$SOURCE/../opi/generate_opi.sh

DEVICE_NAME=${DESTINATION#$2}  
DEVICE_NAME=${DEVICE_NAME:1} #remove first slash from device name e.g. /scope -> scope 
DESTINATION_OPI=$(dirname $2)
mkdir -p $DESTINATION_OPI/opis/$DEVICE_NAME/opi
rsync -arvud --exclude=".svn*" --exclude="*.sh"  $SOURCE/../opi/ $DESTINATION_OPI/opis/$DEVICE_NAME/opi

