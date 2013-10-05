#! /usr/bin/env python
__author__ = 'henningerj'

# #######################################
'''
Note:
QMainWindow allows for funky thinks like menu- and tool-bars
'''

# #######################################

# TODO video-canvas: resize with mainwindow

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

        self.metadata = dict()
        self.metadata['Metadata A'] = metadata_a
        self.metadata['Metadata B'] = metadata_b

        # DEBUG: canvas pixel size
        self.canvas_v = 800
        self.canvas_h = 600
        img = image.fromarray(np.zeros((self.canvas_v, self.canvas_h))).convert('RGB')

        # #######################################
        # GEOMETRY

        width = 800
        height = 600
        offset_left = 50
        offset_top = 50

        max_tab_width = 300
        min_tab_width = 300

        self.setGeometry(offset_left, offset_top, width, height)
        self.setSizePolicy(Qt.QSizePolicy.Maximum, Qt.QSizePolicy.Maximum)
        self.setMinimumSize(width, height)
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
        self.video_canvas.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)

        policy = self.video_canvas.sizePolicy()
        policy.setHeightForWidth(True)
        self.video_canvas.setSizePolicy(policy)
        print self.video_canvas.sizePolicy().hasHeightForWidth()

        self.video_canvas.setScaledContents(True)
        self.video_canvas.setAlignment(Qt.Qt.AlignVCenter | Qt.Qt.AlignHCenter)

        self.tab = QtGui.QTabWidget()
        self.tab.setMinimumWidth(min_tab_width)
        self.tab.setMaximumWidth(max_tab_width)

        self.top_layout.addWidget(self.video_canvas)
        self.top_layout.addWidget(self.tab)

        # #######################################
        # POPULATE TAB
        self.pages = dict()
        for metadata_listname in self.metadata.keys():
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

            for entry_name in self.metadata[metadata_listname].keys():
                entry = Metadata_Entry(metadata_listname, entry_name,
                                       self.metadata[metadata_listname][entry_name], self)
                self.page_scroll_layout.addWidget(entry)

            self.page_scroll.setWidget(self.page_scroll_contents)

        # #######################################
        # CANVAS

        self.video_canvas.setPixmap(QtGui.QPixmap.fromImage(iqt.ImageQt(img).scaled(self.video_canvas.size(),
                                                                                    Qt.Qt.KeepAspectRatio,
                                                                                    Qt.Qt.FastTransformation)))
        # self.video_canvas.setPixmap(QtGui.QPixmap.fromImage(iqt.ImageQt(img).scaled(400, 300)))
        #self.video_canvas.setPixmap(QtGui.QPixmap.fromImage(iqt.ImageQt(img)))

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

        # INITIATE COMPONENTS
        self.controlcenter = ControlCenter()
        self.datacollector = DataCollector()
        self.storage = Storage()

        # CREATE THREADS TO MANAGE THE COMPONENTS
        self.threads = dict()
        self.threads['control'] = QtCore.QThread(self)
        self.threads['data'] = QtCore.QThread(self)
        self.threads['storage'] = QtCore.QThread(self)

        # MOVE COMPONENTS INTO THEIR THREADS
        self.controlcenter.moveToThread(self.threads['control'])
        self.datacollector.moveToThread(self.threads['data'])
        self.storage.moveToThread(self.threads['storage'])

        # HERE, WE START THREATS, NOT THE CLASSES INSIDE !!
        self.threads['control'].start()
        self.threads['data'].start()
        self.threads['storage'].start()

        # #######################################
        # CONNECTIONS

        # connect buttons
        self.connect(self.button_a, QtCore.SIGNAL('clicked()'), self.bt_a)
        self.connect(self.button_b, QtCore.SIGNAL('clicked()'), self.bt_b)
        self.connect(self.button_c, QtCore.SIGNAL('clicked()'), self.bt_c)
        self.connect(self.button_d, QtCore.SIGNAL('clicked()'), self.bt_d)
        self.connect(self.button_e, QtCore.SIGNAL('clicked()'), self.bt_e)
        self.connect(self.button_f, QtCore.SIGNAL('clicked()'), self.bt_f)

        # treads

        # create keyboard shortcuts
        self.create_actions()

        # #######################################
        # #######################################

    #Note:
    #Buttons...
    # ... can be made inactive
    # ... have on/off states
    # ... can change text, color etc
    # depending on program state.

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

    def update_video(self, frame):
        # self.video_canvas.setPixmap(QtGui.QPixmap.fromImage(ImageQt.ImageQt(frame).scaledToWidth(self.canvas_size)))

        pass

    def metadata_changed(self, package):
        print 'metadata changed:', package['listname'], package['entryname'], package['entry']

        # update metadata dictionaries
        self.metadata[package['listname']][package['entryname']] = package['entry']

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

        self.connect(self.lineedit, QtCore.SIGNAL('editingFinished()'), self.data_changed)
        self.connect(self, QtCore.SIGNAL('metadata_changed(PyQt_PyObject)'), parent.metadata_changed)

    def data_changed(self):
        package = dict()
        package['listname'] = self.listname
        package['entryname'] = self.entryname
        package['entry'] = self.lineedit.text()
        self.emit(QtCore.SIGNAL('metadata_changed(PyQt_PyObject)'), package)

# #######################################
# WORKER CLASSES


class ControlCenter(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)


class DataCollector(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)


class Storage(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

# #######################################

if __name__ == "__main__":
    # entering the gui app
    qapp = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    exit(qapp.exec_())
