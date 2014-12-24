#!/usr/bin/python
# monitor.py
# 
# 1. monitor PV corresponding to specific raspi
# 2. 

import numpy as np

class Monitor:
	''' monitor class to listen for broadcast insutrctions
  from network with pv name and camera to stream from '''

	def __init__(self):
		self.staticip = "192.168."

	def testimage(self, x=100, y=100):
		return np.arange(x*y).reshape(x,y)
