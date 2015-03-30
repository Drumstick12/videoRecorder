# TODO try except
import picamera
import warnings
from datetime import datetime

class RasPiCam(object):
	def __init__(self):
		self.camera = None
	
	def open(self):
		self.camera = picamera.PiCamera()
		self.camera.resolution = (1920,1080)
		self.camera.framerate = 30
		self.start_preview()
	
	def close(self):
		self.camera.stop_preview()
		self.camera.close()
		self.camera = None
		
	def is_working(self):
		return self.camera is not None
	
	def start_preview(self):
		self.camera.start_preview()
		self.camera.preview.fullscreen = False
		self.camera.preview.window = (500, 300, 480, 270)
		self.camera.preview_alpha = 230
	
	def stop_preview(self):
		self.camera.stop_preview()
	
	# TODO
	def get_properties(self):
		return None
		
	def get_resolution(self):
		if self.camera is not None:
			return self.camera.resolution
		else:
			raise ValueError("Camera is not opened or not functional! Camera is None")
	
	