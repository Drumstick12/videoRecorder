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
		
		btn_right = QtGui.QPushButton('right')
		preview_control_layout.addWidget(btn_right)
		btn_right.setShortcut('Ctrl+right')
		btn_right.setToolTip('Strg + right')
		btn_right.clicked.connect(camera.move_preview_right)
		
		btn_left = QtGui.QPushButton('left')
		preview_control_layout.addWidget(btn_left)
		btn_left.setShortcut('Ctrl+left')
		btn_left.setToolTip('Strg + left')
		btn_left.clicked.connect(camera.move_preview_left)
		
		btn_up = QtGui.QPushButton('up')
		preview_control_layout.addWidget(btn_up)
		btn_up.setShortcut('Ctrl+up')
		btn_up.setToolTip('Strg + up')
		btn_up.clicked.connect(camera.move_preview_up)
		
		btn_down = QtGui.QPushButton('down')
		preview_control_layout.addWidget(btn_down)
		btn_down.setShortcut('Ctrl+down')
		btn_down.setToolTip('Strg + down')
		btn_down.clicked.connect(camera.move_preview_down)
		
		self.main_layout.addLayout(preview_control_layout)
		
		return
