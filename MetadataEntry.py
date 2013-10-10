__author__ = 'Jan Grewe'
try:
    from PyQt4 import QtGui, QtCore, Qt
except Exception, details:
    print 'Unfortunately, your system misses the PyQt4 packages.'
    quit()

class MetadataEntry(QtGui.QWidget):
    """This class creates label-and-lineedit-combinations in the tabs and allows for feedback communication."""

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

        #self.connect(self.lineedit, QtCore.SIGNAL('editingFinished()'), self.data_changed)
        #self.connect(self, QtCore.SIGNAL('metadata_changed(PyQt_PyObject)'), parent.metadata_changed)

    def data_changed(self):
        package = dict()
        package['listname'] = self.listname
        package['entryname'] = self.entryname
        package['entry'] = self.lineedit.text()
        self.emit(QtCore.SIGNAL('metadata_changed(PyQt_PyObject)'), package)