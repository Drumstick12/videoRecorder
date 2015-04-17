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
			
			if isinstance(att, AttributeNumber):
				sbox = QtGui.QSpinBox(self)
				sbox.setMaximum(att.max)
				sbox.setMinimum(att.min)
				sbox.setValue(att.current)
				self.connect(sbox, QtCore.SIGNAL("valueChanged(int)"), att.handle)
				new_h_layout.addWidget(sbox)
			
			if isinstance(att, AttributeOptions):
				cbox = QtGui.QComboBox(self)
				for entry in att.options:
					cbox.addItem(str(entry))
				cbox.setCurrentIndex(att.default_index)
				self.connect(cbox, QtCore.SIGNAL("currentIndexChanged(QString)"), att.handle)
				new_h_layout.addWidget(cbox)
			
			self.main_layout.addLayout(new_h_layout)
		
		# PREVIEW HELPER STUFF
		preview_control_layout = QtGui.QHBoxLayout()
		label = QtGui.QLabel("Preview Control", self)
		preview_control_layout.addWidget(label)
		
		btn_bigger = QtGui.QPushButton('bigger')
		preview_control_layout.addWidget(btn_bigger)
		btn_bigger.setShortcut('Ctrl+b')
		btn_bigger.setToolTip('Strg + b')
		btn_bigger.clicked.connect(camera.increase_preview)
		
		btn_smaller = QtGui.QPushButton('smaller')
		preview_control_layout.addWidget(btn_smaller)
		btn_smaller.setShortcut('Ctrl+s')
		btn_smaller.setToolTip('Strg + s')
		btn_smaller.clicked.connect(camera.decrease_preview)
		
		self.main_layout.addLayout(preview_control_layout)
		
		return
