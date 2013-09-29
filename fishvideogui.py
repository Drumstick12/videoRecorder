#! /usr/bin/env python
__author__ = 'henninger'

# #######################################

try:
    from PyQt4 import QtGui, QtCore, Qt
except Exception, details:
    print
    'Unfortunately, your system misses the PyQt4 packages.'
    quit()

import os
import sys

# #######################################

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
        self.setFixedSize(width, hight)
        self.setWindowTitle('MediaWiki File-Uploader')

        self.mainLayout = QtGui.QGridLayout()
        self.setLayout(self.mainLayout)

        # #######################################

        # the config
        self.cfg = dict

        # use input arguments
        self.prog_name = sys.argv[0]


# #######################################

if __name__ == "__main__":

    # entering the gui app
    qapp = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    exit(qapp.exec_())
