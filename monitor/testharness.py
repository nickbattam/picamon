#!/usr/bin/python

import unittest
import monitor

class TestMonitor(unittest.TestCase):

	def test_test(self):
		print "hello world"

	def test_attr(self):
		mon = monitor.Monitor()
		assert mon.staticip!=""

	def test_testimage(self):
		mon = monitor.Monitor()
		image = mon.testimage()
		assert len(image) != 0


if __name__ == '__main__':
	unittest.main()
