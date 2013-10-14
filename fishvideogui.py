#! /usr/bin/env python
import sys
import os
import glob
from nitime.index_utils import tri
from VideoRecording import VideoRecording
from default_config import default_template, camera_device_search_range, camera_name_format

sys.path.append('../')
from datetime import date
from MetadataEntry import MetadataEntry
from VideoCanvas import VideoCanvas
from MetadataTab import MetadataTab
import numpy as np
from PIL import Image as image
from PIL import ImageQt as iqt
from Camera import Camera, brg2rgb
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
# TODO Key bindings for start and stop of recording
# TODO validation of meta data tabs. Warn, if info is missing!

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
        self.metadata_tabs = dict()
        self.trial_counter = 0
        self.data_dir = '.'
        # #######################################
        # GEOMETRY of mainwindow at start-up
        width, height = 800, 600
        offset_left, offset_top = 100, 100
        max_tab_width, min_tab_width = 640, 480
        self.fps = 25

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
        self.videos = QtGui.QTabWidget()
        self.videos.setMinimumWidth(min_tab_width)
        self.videos.setMaximumWidth(max_tab_width)
        self.video_recordings = None
        self.video_tabs = {}

        self.metadata = QtGui.QTabWidget()
        self.metadata.setMinimumWidth(min_tab_width)
        self.metadata.setMaximumWidth(max_tab_width)

        self.top_layout.addWidget(self.videos)
        self.top_layout.addWidget(self.metadata)

        # #######################################
        # POPULATE TAB
        self.populate_metadata_tab(default_template)
        self.populate_video_tabs()

        # #######################################
        # POPULATE BOTTOM LAYOUT
        self.button_record = QtGui.QPushButton('Start Recording')
        self.button_stop = QtGui.QPushButton('Stop')
        self.button_cancel = QtGui.QPushButton('Cancel')

        self.button_stop.setDisabled(True)
        self.button_cancel.setDisabled(True)

        self.button_record.setMinimumHeight(50)
        self.button_stop.setMinimumHeight(50)
        self.button_cancel.setMinimumHeight(50)

        self.bottom_layout.addWidget(self.button_record)
        self.bottom_layout.addWidget(self.button_stop)
        self.bottom_layout.addWidget(self.button_cancel)

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
        self.connect(self.button_cancel, QtCore.SIGNAL('clicked()'), self.clicked_cancel)
        self.connect(self.button_record, QtCore.SIGNAL('clicked()'), self.clicked_record)
        self.connect(self.button_stop, QtCore.SIGNAL('clicked()'), self.clicked_stop)

        # tread connections
        # ...

        # create keyboard shortcuts
        self.create_actions()

        # DEBUG
        # a simple timer to create some noise on the canvas
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.update_video)
        self.timer.start(1000./self.fps)


    def create_menu_bar(self):
        self.statusBar()

        exit_action = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtGui.qApp.quit)

        template_select_action = QtGui.QAction('&Select template', self)
        template_select_action.setStatusTip('Select metadata template')
        template_select_action.triggered.connect(self.select_template)

        about_action = QtGui.QAction('&About', self)
        about_action.setStatusTip('About videoRecorder')
        about_action.triggered.connect(self.show_about)

        cam_config_action = QtGui.QAction('&Camera config', self)
        cam_config_action.setStatusTip('Set camera aliases')
        cam_config_action.triggered.connect(self.cam_aliases)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(exit_action)
        config_menu = menu_bar.addMenu('&Configuration')
        config_menu.addAction(template_select_action)
        config_menu.addAction(cam_config_action)
        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(about_action)

        # #######################################
        # #######################################

    def select_template(self):
        path = '%s/templates' %os.path.abspath('.')
        if not os.path.isdir(path):
            path = os.path.abspath('.')

        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open template',path,"XML files (*.xml *.odml)")
        if file_name:
            self.populate_metadata_tab(file_name)

    def cam_aliases(self):

        pass

    def show_about(self):
        #TODO implement this method which shows a new window
        print 'show about dialog'
        pass

    def populate_metadata_tab(self, template):
        try:
            temp = odml.tools.xmlparser.load(template)
        except:
            print ('failed to load metadata template! {0}'.format(template))
            return

        self.metadata_tabs.clear()
        self.metadata.clear()
        for s in temp.sections:
            self.metadata_tabs[s.type] = MetadataTab(s,self.metadata)

    def populate_video_tabs(self):
        tmp = [cam for cam in [Camera(i) for i in camera_device_search_range] if cam.is_working()]
        self.cameras = {camera_name_format % j: v for j,v in enumerate(tmp)}

        if len(self.cameras) > 0:
            for cam_name, cam in self.cameras.items():
                self.video_tabs[cam_name] = VideoCanvas(parent=self)
                self.videos.addTab(self.video_tabs[cam_name], cam_name)
                self.video_tabs[cam_name].setLayout(QtGui.QHBoxLayout())
        else:
            self.videos.addTab(QtGui.QWidget(),"No camera found")

    def create_and_start_new_videorecordings(self):
        # @jan: could choose potentially from PIM1, MJPG, MP42, DIV3, DIVX, U263, I263, FLV1
        # CV_FOURCC('P','I','M','1')    = MPEG-1 codec
        if self.trial_counter == 0:
            self.check_data_dir()
        #trial_name = '%s/trial_%04i' % (self.data_dir, self.trial_counter)
        trial_name = '{0:s}/trial_{1:04d}'.format(self.data_dir, self.trial_counter)
        self.video_recordings = {cam_name:VideoRecording('{0}_{1}.avi'.format(trial_name,cam_name), cam.get_resolution(), self.fps, 'FLV1')
                                 for cam_name, cam in self.cameras.items()}

    def check_data_dir(self):
        today = date.today()
        today_str = today.isoformat()
        self.data_dir = today_str
        try:
            os.mkdir(today_str)
            self.trial_counter = 0
        except:
            tmp = os.listdir(today_str)
            if len(tmp) > 0:
                self.trial_counter = np.amax([int(e.split('_')[1]) for e in [ee.split('.')[0] for ee in tmp]])+1


    def stop_all_recordings(self):
        for v in self.video_recordings.values():
            v.stop()
        self.video_recordings = None


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
    def clicked_record(self):
        self.create_and_start_new_videorecordings()
        self.button_record.setDisabled(True)
        self.button_cancel.setEnabled(True)
        self.button_stop.setDisabled(False)

    def clicked_cancel(self):
        self.clicked_stop()
        trial_name = 'trial_{0:04d}'.format(self.trial_counter-1)
        map(os.remove, glob.glob(self.data_dir+'/'+trial_name+'*'))
        self.check_data_dir()
        self.button_cancel.setEnabled(False)

    def clicked_stop(self):
        self.stop_all_recordings()
        self.button_record.setDisabled(False)
        self.button_stop.setDisabled(True)
        self.button_cancel.setDisabled(True)
        self.save_metadata()
        self.trial_counter += 1

    def save_metadata(self):
        trial_name = 'trial_{0:04d}'.format(self.trial_counter)
        file_list = [f for f in os.listdir(self.data_dir) if f.startswith(trial_name)]
        # create a document
        doc = odml.Document()
        # create dataset section
        ds = odml.Section('datasets','dataset')
        p = odml.Property('files', None)
        ds.append(p)
        for f in file_list:
           p.append('{0}/{1}'.format(self.data_dir,f), dtype='string')
        doc.append(ds)

        for t in self.metadata_tabs.values():
            doc.append(t.metadata())

        for cam_name,cam in self.cameras.items():
            s = odml.Section(cam_name,'hardware/camera')
            for p,v in cam.get_properties().items():
                prop = odml.Property(p,v)
                s.append(prop)
            doc.append(s)

        from odml.tools.xmlparser import XMLWriter
        writer = XMLWriter(doc)
        writer.write_file('{0}/{1}.xml'.format(self.data_dir, trial_name))

    def update_video(self):
        for cam_name,cam in self.cameras.items():
            frame = cam.grab_frame()
            if self.video_recordings is not None:
                self.video_recordings[cam_name].write(frame)
            label = self.videos.tabText(self.videos.currentIndex())

            if label == cam_name:
                self.video_tabs[cam_name].setImage(QtGui.QPixmap.fromImage(iqt.ImageQt(image.fromarray(brg2rgb(frame)))))

    # called by metadata-entries in tabs
    # ADAPT to your needs


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
