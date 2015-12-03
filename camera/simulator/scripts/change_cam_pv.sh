#!/bin/bash

if [ -z "$*" ]; then
    echo "no arguments supplied"
    exit 1
fi


OLD_NAME=$1
NEW_NAME=$2
find $3 -type f -exec sed -i "s/$OLD_NAME/$NEW_NAME/g" {} +
