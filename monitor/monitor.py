#!/usr/bin/python
# monitor.py

import numpy as np
import epics
from epics import pv

from camera import Camera

class Monitor(object):
	''' monitor class to listen for broadcast insutrctions
  from network with pv name and camera to stream from '''

	def __init__(self):
		self.pvprefix = "MON-CONTROL:"
		self.monitorname = "PI1"

		self.camera_name = pv.PV(self.pvprefix + self.monitorname,
			callback=self.update_camera)

	def update_camera(self, value, **kw):
		self.camera.close()
		self.camera = Camera(value)

	def testimage(self, x=100, y=100):
		return np.arange(x*y).reshape(x,y)

	def readPV(self):
		return epics.caget(self.pvprefix + self.monitorname)

  # camonitor the cameraname to know which camera to read
  # camonitor $(PREFIX):CAM1:arrayDate to get image stream
  # camonitor $(PREFIX):CAM1:xsize/ysize to get image size

