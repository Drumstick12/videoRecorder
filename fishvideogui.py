#! /usr/bin/env python
try:
	from PyQt4 import QtGui, QtCore, Qt
except Exception, details:
	print 'Unfortunately, your system misses the PyQt4 packages.'
	quit()
try:
	import wikitools
except Exception, details:
	print 'Unfortunately, your system misses wikitools.'
	quit()
import os,sys

__author__ = 'henninger'

class Main(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)

		# #######################################

		# GEOMETRY
		width = 600
		hight = 700
		offsetLeft = 50
		offsetTop = 50

		self.setGeometry(offsetLeft, offsetTop, width, hight)
		self.setFixedSize(width,hight)
		self.setWindowTitle('MediaWiki File-Uploader')

		self.mainLayout = QtGui.QGridLayout()
		self.setLayout( self.mainLayout )

		# #######################################

		# the config
		self.cfg = {}
		self.cfg['cfg_file'] = '.mw_file_uploader.cfg'
		self.cfg['cfg_options'] = ['wiki_paths', 'users']

		# use input arguments
		self.prog_name = sys.argv[0]
