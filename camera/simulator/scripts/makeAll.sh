#!/bin/bash

if [ -z "$*" ]; then
    echo "no arguments supplied"
    exit 1
fi

for camera in 'find $1 -mindepth 1 -maxdepth 1 -type d'
do
   cd $camera
   make clean uninstall
   make 
done
