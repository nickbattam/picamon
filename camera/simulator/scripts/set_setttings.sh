#!/bin/bash

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
    value=${param[1]}

    # set value using caput
    caput $pv_name $value

done < $CONFIG
