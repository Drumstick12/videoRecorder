#! /usr/bin/env python
__author__ = 'henninger'

# #######################################
'''
Note:
QMainWindow allows for funky thinks like menu- and tool-bars
'''

# #######################################

# TODO make list of todos

# #######################################

try:
    from PyQt4 import QtGui, QtCore, Qt
except Exception, details:
    print
    'Unfortunately, your system misses the PyQt4 packages.'
    quit()

# import os
import sys
import numpy as np
from PIL import Image as image
from PIL import ImageQt as iqt

# #######################################


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # #######################################
        # GEOMETRY

        width = 800
        hight = 600
        offset_left = 50
        offset_top = 50

        self.setGeometry(offset_left, offset_top, width, hight)
        self.setSizePolicy(Qt.QSizePolicy.Maximum, Qt.QSizePolicy.Maximum)
        self.setMinimumSize(width, hight)
        self.setWindowTitle('Fish Video GUI')

        # #######################################
        # LAYOUTS

        self.main = QtGui.QWidget()
        self.setCentralWidget(self.main)

        self.main_layout = QtGui.QVBoxLayout()
        self.main.setLayout(self.main_layout)

        self.top_layout = QtGui.QHBoxLayout()
        self.bottom_layout = QtGui.QHBoxLayout()

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)

        # #######################################
        # POPULATE TOP LAYOUT

        self.video_canvas = QtGui.QLabel(self)
        self.tab = QtGui.QTabWidget()
        self.page_a = QtGui.QWidget()
        self.page_b = QtGui.QWidget()
        self.tab.addTab(self.page_a, "MetaData A")
        self.tab.addTab(self.page_b, "MetaData B")

        self.top_layout.addWidget(self.video_canvas)
        self.top_layout.addWidget(self.tab)

        # #######################################
        # tab page a
        self.page_a_layout = QtGui.QHBoxLayout()
        self.page_a.setLayout(self.page_a_layout)

        self.page_a_scroll = Qt.QScrollArea()
        self.page_a_layout.addWidget(self.page_a_scroll)

        self.page_a_scroll_contents = QtGui.QWidget()
        self.page_a_scroll.setWidget(self.page_a_scroll_contents)

        self.page_a_scroll_layout = QtGui.QVBoxLayout(self.page_a_scroll_contents)
        self.page_a_scroll_contents.setLayout(self.page_a_scroll_layout)

        self.page_a_scroll.setLayout(self.page_a_scroll_layout)

        self.page_a_scroll.setWidgetResizable(True)
        for i in xrange(25):
            label = QtGui.QCheckBox()
            self.page_a_scroll_layout.addWidget(label)

        # #######################################
        # canvas

        # DEBUG: canvas pixel size
        canvas_v = 800
        canvas_h = 600
        # DEBUG: canvas start image
        img = image.fromarray(np.zeros((canvas_v, canvas_h))).convert('RGB')

        self.video_canvas.setPixmap(QtGui.QPixmap.fromImage(iqt.ImageQt(img).scaled(400, 300)))
        # self.video_canvas.setPixmap(QtGui.QPixmap.fromImage(iqt.ImageQt(img)))
        self.video_canvas.setAlignment(Qt.Qt.AlignVCenter | Qt.Qt.AlignHCenter)

        # #######################################
        # POPULATE BOTTOM LAYOUT

        self.button_a = QtGui.QPushButton('Button A')
        self.button_b = QtGui.QPushButton('Button B')
        self.button_c = QtGui.QPushButton('Button C')
        self.button_d = QtGui.QPushButton('Button D')

        self.button_a.setMinimumHeight(50)
        self.button_b.setMinimumHeight(50)
        self.button_c.setMinimumHeight(50)
        self.button_d.setMinimumHeight(50)

        self.bottom_layout.addWidget(self.button_a)
        self.bottom_layout.addWidget(self.button_b)
        self.bottom_layout.addWidget(self.button_c)
        self.bottom_layout.addWidget(self.button_d)

        # #######################################

        # the config
        # self.cfg = dict

        # use input arguments
        self.prog_name = sys.argv[0]


# #######################################

if __name__ == "__main__":
    # entering the gui app
    qapp = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    exit(qapp.exec_())
