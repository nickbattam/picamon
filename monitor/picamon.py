#!/usr/bin/env python
# Main launch script for PiCaMon monitors
from controller import Controller
from monitor import Monitor
from plotter_pygame import PyGamePlotter
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--prefix', required=True, dest='prefix', help='controller IOC prefix')
parser.add_argument('--name', required=True, dest='name', help='name of monitor')
parser.add_argument('--fullscreen', dest='fullscreen', type=bool, default=False, help='True for fullscreen (default), False for small window')
args = parser.parse_args()

controller = Controller(args.prefix, args.name)
plotter = PyGamePlotter(args.name, args.fullscreen)
monitor = Monitor(plotter, controller)

monitor.start()
plotter.quit()

