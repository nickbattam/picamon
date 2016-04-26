#!/usr/bin/env python

import sys
import os
import argparse
import ConfigParser
import epicsdbbuilder

def read_single(parser, category, variable):
    return parser.get(category, variable)

def read_list(parser, category, variable, delimiter):
    data = parser.get(category, variable).split(delimiter)   
    data = map(str.strip, data)
    return data

def generate_monitor_subfile(filename, monitors, prefix):
    monitor_subfile = open(filename, 'w')
    monitor_subfile.write("file \"${TOP}/db/monitor.db\" {\n")
    monitor_subfile.write("\tpattern { p, monitor }\n")
    for monitor in monitors: monitor_subfile.write("\t{ %s, %s }\n" % (prefix, monitor) )
    monitor_subfile.write("}\n")
    monitor_subfile.close()

def generate_general_subfile(filename, prefix):
    general_subfile = open(filename, 'w')
    general_subfile.write("file \"${TOP}/db/general.db\" {\n")
    general_subfile.write("\tpattern { p }\n")
    general_subfile.write("\t{ %s }\n" % prefix )
    general_subfile.write("}\n")
    general_subfile.close()

def generate_list_file(filename, elements):
    list_file = open(os.path.join(boot,filename), 'w')
    for element in elements: list_file.write("%s\n" % element)
    list_file.close()

def getIOCboot():
    top = os.path.dirname(sys.argv[0])
    for i in os.listdir(top):
        if i.startswith("ioc"):
            for j in os.listdir(os.path.join(top,i)):
                if j.startswith("ioc"):
                    return os.path.join(top,i,j)      
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Configure PiCaMon Controller IOC')
    parser.add_argument('--config', dest='config_file', help='configuration file')
    args = parser.parse_args()
    if not args.config_file: parser.error("Missing configuration file")

    # read config file
    cp = ConfigParser.ConfigParser()
    cp.read(args.config_file)
    prefix = read_single(cp, "controller", "prefix")
    cameras = read_list(cp, "cameras", "name", ',')
    monitors = read_list(cp, "monitors", "name", ',')

    ## generate substitution files
    boot = getIOCboot()
    generate_monitor_subfile(os.path.join(boot,"monitor.substitutions"), monitors, prefix)
    generate_general_subfile(os.path.join(boot,"general.substitutions"), prefix)

    ## generate camera & monitor list files (to be read by aSub PV at startup)
    generate_list_file("camera.list", cameras)
    generate_list_file("monitor.list", monitors)

