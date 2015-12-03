#!/bin/bash

# to run: ./save_settings_to_file.sh input.txt > output.txt

set -e
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

if [ -z "$*" ]; then
    echo "no arguments supplied. 1:configfile"
    exit 1
fi

CONFIG=$(readlink -f $1)

while read -a param ; do

    # skip empty line
    [[ -z ${param[0]} ]] && continue

    # skip line starting with #
    [[ ${param[0]} =~ ^#.* ]] && continue

    # get parameters from config file
    pv_name=${param[0]}

    caget $pv_name:cam1:Model_RBV
    #caget $pv_name:cam1:Gain
    #caget $pv_name:cam1:AcquireTime
    #caget $pv_name:ROI1:ReverseX
    #caget $pv_name:ROI1:ReverseY
    #caget $pv_name:FLIP_X
    #caget $pv_name:FLIP_Y
    #caget $pv_name:SOFT_REF_USE
    #caget $pv_name:SOFT_REF_X
    #caget $pv_name:SOFT_REF_Y
    #caget $pv_name:PROF_USE
    #caget $pv_name:Stats1:CursorX
    #caget $pv_name:Stats1:CursorY
    #caget $pv_name:UseCustomCentroid
    #caget $pv_name:Centroid1:ThreshStart
    #caget $pv_name:Centroid1:ThreshIncr
    #caget $pv_name:Centroid1:MinPxlFract
    #caget $pv_name:Centroid1:MaxPxlFract
    #caget $pv_name:Centroid1:Successive
    #caget $pv_name:Centroid1:SmoothMethodSel
    #caget $pv_name:Centroid1:SmoothSigmaX
    #caget $pv_name:Centroid1:SmoothSigmaY
    #caget $pv_name:Centroid1:UseDownsamWidth
    #caget $pv_name:Centroid1:UseDownsamHeight
    #caget $pv_name:Centroid1:DownsamWidth
    #caget $pv_name:Centroid1:DownsamHeight
    #caget $pv_name:Centroid1:UseContour
    #caget $pv_name:Centroid1:UseRectangle
    #caget $pv_name:Centroid1:MethodDist

done < $CONFIG
