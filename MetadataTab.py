__author__ = 'Jan Grewe'
try:
    from PyQt4 import QtGui, QtCore, Qt
except Exception, details:
    print 'Unfortunately, your system misses the PyQt4 packages.'
    quit()

from odml import *
from MetadataEntry import MetadataEntry

class MetadataTab(QtGui.QWidget):
    """This class creates label-and-lineedit-combinations in the tabs and allows for feedback communication."""

    def __init__(self, section, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.layout = QtGui.QHBoxLayout()
        self.setLayout(self.layout)
        self.page_scroll = Qt.QScrollArea()
        self.layout.addWidget(self.page_scroll)
        self.scroll_contents = QtGui.QWidget()
        self.scroll_layout = QtGui.QVBoxLayout(self.scroll_contents)
        self.parent.addTab(self, section.type)
        self.create_tab(section)

    def create_tab(self, section):

        self.scroll_contents.setLayout(self.scroll_layout)
        self.page_scroll.setWidgetResizable(False)

        self.populate_tab(section)
        self.page_scroll.setWidget(self.scroll_contents)



    def populate_tab(self, section):
        for p in section.properties:
            print p.name
            entry = MetadataEntry(section.type, p.name, p.value.value, self.parent)
            self.scroll_layout.addWidget(entry)

