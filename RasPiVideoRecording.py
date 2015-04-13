import picamera
import cPickle as pickle

class RasPiVideoRecording(object):
	def __init__(self, filename, filename_metadata, codec, raspicam):
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