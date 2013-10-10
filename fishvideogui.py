#! /usr/bin/env python
import sys
sys.path.append('../')

from MetadataEntry import MetadataEntry
from VideoCanvas import VideoCanvas
import numpy as np
from PIL import Image as image
from PIL import ImageQt as iqt
from Camera import Camera
__author__ = 'Joerg Henninger, Jan Grewe, Fabian Sinz'

# #######################################
'''
Note:
QMainWindow allows for funky things like menu- and tool-bars

Keyboard Shortcuts:
Quit Program: ESC
Next Metadata-Tab: CTRL+Page-Down
Previous Metadata-Tab: CTRL+Page-UP
'''

# #######################################

# TODO video-canvas: full screen does not work properly. why?

# #######################################

try:
    from PyQt4 import QtGui, QtCore, Qt
except Exception, details:
    print 'Unfortunately, your system misses the PyQt4 packages.'
    quit()

# import os
try:
    import odml
except:
    sys.path.append('/usr/lib/python2.7/site-packages')
    try:
        import odml
    except:
        print 'Cannot import odml library for metadata support! Check https://github.com/G-Node/python-odml'
        quit()



# #######################################
# THE MAIN GUI WINDOW


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # #######################################
        # GEOMETRY of mainwindow at start-up

        width, height = 800, 600
        offset_left, offset_top = 100, 100
        max_tab_width, min_tab_width = 500, 500


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

        self.video_canvas = VideoCanvas(parent=self)

        self.tab = QtGui.QTabWidget()
        self.tab.setMinimumWidth(min_tab_width)
        self.tab.setMaximumWidth(max_tab_width)

        self.top_layout.addWidget(self.video_canvas)
        self.top_layout.addWidget(self.tab)

        # camera @fabee: detect cameras and create tabs
        self.cameras = [Camera()]
        for c in self.cameras:
            c.open()


        # #######################################
        # POPULATE TAB
        self.populateMetadataTab('./templates/decision_template.xml')

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
        self.create_menu_bar()

        # #######################################
        # WORKER THREADS
        # For heavy duty work, which might block the GUI.
        # Some typical applications are examplified.
        # Often, these processes act on different time-scales.

        # INITIATE WORKER COMPONENTS
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

        # HERE, WE START THREATS, NOT THE INSTANCES INSIDE !!
        self.threads['control'].start()
        self.threads['data'].start()
        self.threads['storage'].start()

        # #######################################
        # CONNECTIONS
        # These are necessary to connect GUI elements and instances in various threads.
        # Signals and slots can easily be custom-crafted to meet the needs. Data can be sent easily, too.

        # connect buttons
        self.connect(self.button_a, QtCore.SIGNAL('clicked()'), self.bt_a)
        self.connect(self.button_b, QtCore.SIGNAL('clicked()'), self.bt_b)
        self.connect(self.button_c, QtCore.SIGNAL('clicked()'), self.bt_c)
        self.connect(self.button_d, QtCore.SIGNAL('clicked()'), self.bt_d)
        self.connect(self.button_e, QtCore.SIGNAL('clicked()'), self.bt_e)
        self.connect(self.button_f, QtCore.SIGNAL('clicked()'), self.bt_f)

        # tread connections
        # ...

        # create keyboard shortcuts
        self.create_actions()

        # DEBUG
        # a simple timer to create some noise on the canvas
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.update_video)
        self.timer.start(1000./50.)


    def create_menu_bar(self):
        exit_action = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setToolTip('Exit application')
        exit_action.triggered.connect(QtGui.qApp.quit)

        template_select_action = QtGui.QAction('&Select template', self)
        template_select_action.setToolTip('Select metadata template')
        template_select_action.triggered.connect(self.selectTemplate)

        about_action = QtGui.QAction('&About', self)
        about_action.setToolTip('About videoRecorder')
        about_action.triggered.connect(self.showAbout)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(exit_action)
        config_menu = menu_bar.addMenu('&Configuration')
        config_menu.addAction(template_select_action)
        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(about_action)

        # #######################################
        # #######################################

    def selectTemplate(self):
        print 'select template!'
        # TODO implement this mehtod as file select dialog....
        pass

    def showAbout(self):
        #TODO implement this method which shows a new window
        print 'show about dialog'
        pass

    def populateMetadataTab(self, template):
        try:
            temp = odml.tools.xmlparser.load(template)
        except:
            print ('failed to load metadata template! {0}'.format(template))
            return

        self.pages = dict()
        for s in temp.sections:
            self.create_tab(s)

    def create_tab(self, section):
        """

        @param section:
        """
        self.pages[section.type] = (QtGui.QWidget())
        self.tab.addTab(self.pages[section.type], section.type)
        self.page_layout = QtGui.QHBoxLayout()
        self.pages[section.type].setLayout(self.page_layout)

        self.page_scroll = Qt.QScrollArea()
        self.page_layout.addWidget(self.page_scroll)
        self.page_scroll_contents = QtGui.QWidget()
        self.page_scroll_layout = QtGui.QVBoxLayout(self.page_scroll_contents)
        self.page_scroll_contents.setLayout(self.page_scroll_layout)
        self.page_scroll.setWidgetResizable(False)

        self.populate_tab(section)
        self.page_scroll.setWidget(self.page_scroll_contents)

    def populate_tab(self, section):
        for p in section.properties:
            entry = MetadataEntry(section.type, p.name, p.value.value, self)
            self.page_scroll_layout.addWidget(entry)

    #Note:
    #Buttons...
    # ... can be made inactive
    # ... have on/off states
    # ... can change text, color etc
    # depending on program state.
    # Threads..
    # ... have to be connected with Signals/Slots to be independent, i.e. non-blocking.

    # GUI OBJECT CONNECTORS
    # Fill-up!
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

    # call this to update the video-canvas
    def update_video(self, img=None):
        # if no image is given, this method creates random noise
        if img is None:
            img = image.fromarray(
                np.random.random((self.video_canvas.canvas_h, self.video_canvas.canvas_w)) * 256).convert('RGB')

        # update canvas

        #self.video_canvas.setImage(QtGui.QPixmap.fromImage(iqt.ImageQt(img)))
        frame = image.fromarray(self.cameras[0].grab_frame())
        self.video_canvas.setImage(QtGui.QPixmap.fromImage(iqt.ImageQt(frame)))

    # called by metadata-entries in tabs
    # ADAPT to your needs
    def metadata_changed(self, package):
        # update metadata dictionaries
        #self.metadata[package['listname']][package['entryname']] = package['entry']

        # instead of showing this here, you could update your running program or whatever
        #print 'metadata changed:', package['listname'], package['entryname'], package['entry']
        pass

    # ACTIONS
    # Actions can be used to assign keyboard-shortcuts
    # This method is called in the __init__ method to create keyboard shortcuts
    def create_actions(self):
        # EXAMPLE
        # Close Program
        self.action_cancel = QtGui.QAction("Cancel Program", self)
        self.action_cancel.setShortcut(Qt.Qt.Key_Escape)
        self.connect(self.action_cancel, QtCore.SIGNAL('triggered()'), qapp, QtCore.SLOT("quit()"))
        self.addAction(self.action_cancel)

        # Change Tabs
        self.action_change_tab_left = QtGui.QAction("Go one tab to the right", self)
        self.action_change_tab_left.setShortcut(Qt.Qt.CTRL + Qt.Qt.Key_PageDown)
        self.connect(self.action_change_tab_left, QtCore.SIGNAL('triggered()'), self.next_tab)
        self.addAction(self.action_change_tab_left)

        self.action_change_tab_right = QtGui.QAction("Go one tab to the left", self)
        self.action_change_tab_right.setShortcut(Qt.Qt.CTRL + Qt.Qt.Key_PageUp)
        self.connect(self.action_change_tab_right, QtCore.SIGNAL('triggered()'), self.prev_tab)
        self.addAction(self.action_change_tab_right)


    def next_tab(self):
        if self.tab.currentIndex() + 1 < self.tab.count():
            self.tab.setCurrentIndex(self.tab.currentIndex() + 1)
        else:
            self.tab.setCurrentIndex(0)

    def prev_tab(self):
        if self.tab.currentIndex() > 0:
            self.tab.setCurrentIndex(self.tab.currentIndex() - 1)
        else:
            self.tab.setCurrentIndex(self.tab.count() - 1)





# #######################################
# GUI HELPER CLASSES






# #######################################
# WORKER CLASSES


class ControlCenter(QtCore.QObject):
    """Put your experiment logic here."""

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)


class DataCollector(QtCore.QObject):
    """Collect your data in this class."""

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)


class Storage(QtCore.QObject):
    """use this class to store your data periodically."""

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

# #######################################

if __name__ == "__main__":
    # entering the gui app
    qapp = QtGui.QApplication(sys.argv)  # create the main application
    main = Main()  # create the mainwindow instance
    main.show()  # show the mainwindow instance
    exit(qapp.exec_())  # start the event-loop: no signals are sent or received without this.
