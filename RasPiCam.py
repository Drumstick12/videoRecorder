# TODO try except?
try:
	import picamera
	import picamera.array
except:
	pass
	
import io
import numpy as np
import cv2
import time
import warnings
from datetime import datetime

class RasPiCam(object):
	def __init__(self):
		self.camera = None
		self.cv2_stream = None 
		
		self.rec_resolution = (1920,1080)
		# self.rec_resolution = (640,480)
		self.rec_framerate = 30
		
		# (576,324)
		# fitting: (490,275)
		self.preview_width = 480
		self.preview_height = 270
		self.open()
	
	def open(self):
		try:
			self.camera = picamera.PiCamera()
		except:
			self.camera = None
			return
		
		self.camera.resolution = self.rec_resolution
		self.camera.framerate = self.rec_framerate
		self.start_preview()
		
		# time.sleep(1)
		# self.cv2_stream = picamera.array.PiRGBArray(self.camera)
		# self.cv2_stream = io.BytesIO()
		# self.camera.start_recording(self.cv2_stream, format='h264', quality=23)
		# self.camera.capture_continuous(self.cv2_stream, format='bgr')
		# self.camera.capture(self.cv2_stream, format='bgr')
	
	def close(self):
		self.camera.stop_preview()
		self.camera.close()
		self.camera = None
		
	def is_working(self):
		return self.camera is not None
	
	# worker method
	def is_connected(self):
		try:
			test_cam = picamera.PiCamera()
			test_cam.close()
			return True
		except:
			return False
	
	def start_preview(self):
		self.camera.start_preview()
		self.camera.preview.fullscreen = False
		self.camera.preview.window = (100, 300, self.preview_width, self.preview_height)
		# self.camera.preview_alpha = 245
	
	def stop_preview(self):
		self.camera.stop_preview()
	
	def increase_preview(self):
		self.preview_width += 16
		self.preview_height += 9
		self.camera.preview.window = (100, 300, self.preview_width, self.preview_height)
	
	def decrease_preview(self):
		self.preview_width -= 16
		self.preview_height -= 9
		self.camera.preview.window = (100, 300, self.preview_width, self.preview_height)
	
	def grab_frame(self):
		frame = np.zeros((self.preview_height,self.preview_width,3), np.uint8)
		dtime = datetime.now()
		# self.camera.capture(self.cv2_stream, format='bgr')
		# frame = self.cv2_stream.array
		# print frame
		# print frame.shape
	        # cv2.imshow("test", frame)
		# cv2.waitKey(0)
		# self.cv2_stream.truncate(0)
		# self.cv2_stream.seek(0)
		return frame, dtime
	
	# TODO
	def get_properties(self):
		ret = {}
		ret["rasp_framerate"] = self.camera._get_framerate()
		return ret
	
	def is_raspicam(self):
		return True
		
	def get_resolution(self):
		if self.camera is not None:
			return self.camera.resolution
		else:
			raise ValueError("Camera is not opened or not functional! Camera is None")
	
	def get_fps(self):
		return self.camera.framerate
	
	