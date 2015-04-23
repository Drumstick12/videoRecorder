try:
    from PyQt4 import QtGui, QtCore, Qt
except Exception, details:
    print 'Unfortunately, your system misses the PyQt4 packages.'
    quit()
import picamera
import cPickle as pickle

class RasPiVideoRecording(QtCore.QObject):
	def __init__(self, filename, filename_metadata, codec, raspicam):
		QtCore.QObject.__init__(self)
		# super(RasPiVideoRecording, self).__init__(self) #??!!!
		self.cam = raspicam
		self.filename = filename
		self.filename_metadata = filename_metadata
		
		self.cam.camera.start_recording(filename, format=codec)
	
	def write(self, x):
		pass
	
	def write_metadata(self, current_datetime):
		with open(self.filename_metadata, 'ab') as f:
			# pickle.dump(current_datetime, f)
			f.flush()
		
	def stop(self):
		self.cam.camera.stop_recording()