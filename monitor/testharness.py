#!/usr/bin/python

import unittest
import monitor

class TestMonitor(unittest.TestCase):

	def test_attr(self):
		mon = monitor.Monitor()
		assert mon.pvprefix == "MON-CONTROL:"
		assert mon.monitorname == "PI1"

	def test_testimage(self):
		mon = monitor.Monitor()
		image = mon.testimage()
		assert len(image) != 0
#		print image

	def test_readPV(self):
		mon = monitor.Monitor()
		pv_result = mon.readPV()
		assert pv_result == "CAM1"


if __name__ == '__main__':
	unittest.main()
