#! /usr/bin/env python
__author__ = 'henningerj'

# #######################################
'''
Notes:
QMainWindow allows for funky thinks like menu- and tool-bars
'''

# #######################################

# TODO video-canvas: resize with mainwindow
# TODO Metadata: read-in and show metadata-entries for dictionary of dictionary and connect to source-dictonaries
# TODO create structure for worker-threads: data-thread, control-thread

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
        # ORGANIZATION

        # the config
        # self.cfg = dict()

        # use input arguments
        self.prog_name = sys.argv[0]


        # some debugging stuff
        metadata_a = dict()
        metadata_b = dict()

        metadata_a['A'] = 0
        metadata_a['B'] = 'stuff'
        metadata_a['C'] = 'lots of stuff'

        metadata_b['A'] = 1
        metadata_b['B'] = 'more stuff'
        metadata_b['C'] = 'really a lot of stuff'

        metadata = dict()
        metadata['Metadata A'] = metadata_a
        metadata['Metadata B'] = metadata_b

        # #######################################
        # GEOMETRY

        width = 800
        hight = 600
        offset_left = 50
        offset_top = 50

        max_tab_width = 300

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
        self.tab.setMaximumWidth(max_tab_width)

        self.top_layout.addWidget(self.video_canvas)
        self.top_layout.addWidget(self.tab)

        # populate tab
        self.pages = dict()
        for metadata_listname in metadata.keys():
            self.pages[metadata_listname] = (QtGui.QWidget())
            self.tab.addTab(self.pages[metadata_listname], metadata_listname)

            self.page_layout = QtGui.QHBoxLayout()
            self.pages[metadata_listname].setLayout(self.page_layout)

            self.page_scroll = Qt.QScrollArea()
            self.page_layout.addWidget(self.page_scroll)

            self.page_scroll_contents = QtGui.QWidget()

            self.page_scroll_layout = QtGui.QVBoxLayout(self.page_scroll_contents)
            self.page_scroll_contents.setLayout(self.page_scroll_layout)

            self.page_scroll.setWidgetResizable(False)

            for entry_name in metadata[metadata_listname].keys():
                entry = Metadata_Entry(metadata_listname, entry_name, metadata[metadata_listname][entry_name])
                self.page_scroll_layout.addWidget(entry)

            self.page_scroll.setWidget(self.page_scroll_contents)

        # #######################################
        # CANVAS

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

        self.button_a = QtGui.QPushButton('Start Recording')
        self.button_b = QtGui.QPushButton('Stop')
        self.button_c = QtGui.QPushButton('Play')
        self.button_d = QtGui.QPushButton('Save')
        self.button_e = QtGui.QPushButton('Discard')
        self.button_f = QtGui.QPushButton('Comment')

        self.button_a.setMinimumHeight(50)
        self.button_b.setMinimumHeight(50)
        self.button_c.setMinimumHeight(50)
        self.button_d.setMinimumHeight(50)
        self.button_e.setMinimumHeight(50)
        self.button_f.setMinimumHeight(50)

        self.bottom_layout.addWidget(self.button_a)
        self.bottom_layout.addWidget(self.button_b)
        self.bottom_layout.addWidget(self.button_c)
        self.bottom_layout.addWidget(self.button_d)
        self.bottom_layout.addWidget(self.button_e)
        self.bottom_layout.addWidget(self.button_f)

        # #######################################
        # WORKER THREADS

        # #######################################
        # CONNECTIONS

        # connect buttons
        self.connect(self.button_a, QtCore.SIGNAL('clicked()'), self.bt_a)
        self.connect(self.button_b, QtCore.SIGNAL('clicked()'), self.bt_b)
        self.connect(self.button_c, QtCore.SIGNAL('clicked()'), self.bt_c)
        self.connect(self.button_d, QtCore.SIGNAL('clicked()'), self.bt_d)
        self.connect(self.button_e, QtCore.SIGNAL('clicked()'), self.bt_e)
        self.connect(self.button_f, QtCore.SIGNAL('clicked()'), self.bt_f)

        # create keyboard shortcuts
        self.create_actions()

        # #######################################

    '''
    Note:
    Buttons...
     ... can be made inactive
     ... have on/off states
     ... can change text, color etc
     depending on program state.
    '''

    # GUI OBJECT CONNECTORS
    def bt_a(self):
        pass

    def bt_b(self):
        pass

    def bt_c(self):
        pass

    def bt_d(self):
        pass

    def bt_e(self):
        pass

    def bt_f(self):
        pass

    def update_video(self):
        pass

    # ACTIONS
    def create_actions(self):
        # EXAMPLE
        # Close Program
        self.action_cancel = QtGui.QAction("Cancel Program", self)
        self.action_cancel.setShortcut(Qt.Qt.Key_Escape)
        self.connect(self.action_cancel, QtCore.SIGNAL('triggered()'), qapp, QtCore.SLOT("quit()"))
        self.addAction(self.action_cancel)

        # FUNCTIONS

# #######################################


class Metadata_Entry(QtGui.QWidget):
    def __init__(self, listname, entryname, entry, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.listname = listname
        self.entryname = entryname

        self.label = QtGui.QLabel(entryname + ':')
        self.lineedit = QtGui.QLineEdit(str(entry))

        self.layout = QtGui.QHBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineedit)

# #######################################

if __name__ == "__main__":
    # entering the gui app
    qapp = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    exit(qapp.exec_())
