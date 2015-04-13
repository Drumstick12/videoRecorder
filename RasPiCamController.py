class RasPiCamController(object):
	def __init__(self, raspicam):
		self.cam = raspicam
		#print self.cam._get_camera_settings()
	
	def set_brightness(self, value):
		if not 0 <= value <= 100:
			print "brightness value must be within 0 ... 100. Default: 50"
			return
		self.cam.brightness = value
		
	def set_contrast(self, value):
		if not -100 <= value <= 100:
			print "contrast value must be within -100 ... 100. Default: 0"
			return
		self.cam.contrast = value
	
	def set_exposure_compensation(self, value):
		"""
		Sets the exposure compensation to given value. Higher values result in brighter images.
		"""
		if not -25 <= value <= 25:
			print "exposure compensation must be within -25 ... 25. Default: 0"
			return
		self.cam.exposure_compensation = value
	
	def set_exposure_mode(self, mode):
		modes = ['off', 'auto', 'night',  'nightpreview', 'backlight', 'spotlight', 
					'sports', 'snow', 'beach', 'verylong', 'fixedfps', 'antishake', 'fireworks']
		if mode not in modes:
			print "Mode must be one of: " + str(modes) + "\nDefault: auto"
			return
		self.cam.exposure_mode = mode
	
	def set_iso(self, value):
		values = [100, 200, 400, 800]
		if value not in values:
			print "value must be one of " + str(values) + " Default: 100"
		self.cam.iso = value
		
	def set_meter_mode(self, mode):
		"""
		Sets the mode to determine the camera uses to determine exposure time. Default: average
		"""
		modes = ['average', 'spot', 'backlit', 'matrix']
		if mode not in modes:
			print "Mode must be one of: " + str(modes) + "\nDefault: average"
			return
		self.cam.meter_mode = mode 