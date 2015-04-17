from RasPiCamController import Attribute, AttributeNumber, AttributeOptions

try:
    from PyQt4 import QtGui, QtCore, Qt
except Exception, details:
    print 'Unfortunately, your system misses the PyQt4 packages.'
    quit()

class RasPiCamControllerTab(QtGui.QWidget):
	def __init__(self, camera):
		super(RasPiCamControllerTab, self).__init__()
		
		self.main_layout = QtGui.QVBoxLayout()
		self.setLayout(self.main_layout)
		
		for att in camera.cam_controller.attributes:
			new_h_layout = QtGui.QHBoxLayout()
			label_name = QtGui.QLabel(att.name, self)
			new_h_layout.addWidget(label_name)
			
			# TODO add spinbox/dropdown menu
			if isinstance(att, AttributeNumber):
				sbox = QtGui.QSpinBox(self)
				sbox.setMaximum(att.max)
				sbox.setMinimum(att.min)
				sbox.setValue(att.current)
				new_h_layout.addWidget(sbox)
			
			if isinstance(att, AttributeOptions):
				cbox = QtGui.QComboBox(self)
				for entry in att.options:
					cbox.addItem(str(entry))
				cbox.setCurrentIndex(att.default_index)
				new_h_layout.addWidget(cbox)
			# TODO connect spinbox/dropdown with handle
			
			self.main_layout.addLayout(new_h_layout)
		return
